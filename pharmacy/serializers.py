from rest_framework import serializers
from .models import Medicine, Prescription, PrescriptionItem
from billing.models import Invoice
from audit.utils import log_action

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), source='medicine', write_only=True
    )
    
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine_id', 'medicine_name', 'quantity', 'availability_status']
        read_only_fields = ['availability_status']

class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True)
    
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'dentist', 'treatment', 'created_at', 'items']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        prescription = Prescription.objects.create(**validated_data)
        
        available_items_cost = 0
        
        for item_data in items_data:
            medicine = item_data['medicine']
            quantity = item_data['quantity']
            
            if medicine.stock_quantity >= quantity:
                availability = 'available'
                available_items_cost += medicine.price * quantity
                # We don't reduce stock here, we reserve it or reduce on dispense
            else:
                availability = 'not_available'
                
            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine=medicine,
                quantity=quantity,
                availability_status=availability
            )
            
        # Generate Invoice if there are available items
        if available_items_cost > 0:
            invoice = Invoice.objects.create(
                patient=prescription.patient,
                prescription=prescription,
                total_amount=available_items_cost,
                payment_status='pending',
                invoice_type='pharmacy'
            )
            request = self.context.get('request')
            if request is not None and request.user.is_authenticated:
                log_action(request.user, 'Pharmacy invoice created', f'Pharmacy invoice #{invoice.id} created for prescription #{prescription.id}.')

        return prescription
