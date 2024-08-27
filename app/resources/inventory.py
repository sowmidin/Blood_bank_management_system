from flask_restx import Namespace,Resource,fields
from app import db
from app.models import Donor,BloodDatabase
from .permissions import is_admin_or_donor_manager
from app.utils import token_required
from flask import request

Blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
inventory_ns = Namespace('inventory',description="Blood Database management")

inventory_model = inventory_ns.model('BloodDatabase', {
    'blood_group': fields.String(required=True, description='Blood group name',example='A+'),
    'units': fields.Integer(required=True, description='Number of units donated')
})

admin_model = inventory_ns.model('Admin',{
    "message":fields.String(required=True)

})

@inventory_ns.route('/')
class Inventory(Resource):

    
    @inventory_ns.marshal_with(inventory_model)
    @token_required
    def get(self):
        blood_inventory = BloodDatabase.query.all()
        return blood_inventory

    @inventory_ns.expect(inventory_model)
    #@inventory_ns.marshal_with(inventory_model)
    @token_required
    def post(self):
        data = request.get_json()
        print(data)
        blood_group_name = data.get('blood_group')
        if blood_group_name not in Blood_groups:
            return {'message':f'Invalid blood group . Please select from {Blood_groups}'},400
        blood_group_name = str(blood_group_name)
        quantity = data.get('units')
        blood_type = BloodDatabase.query.filter_by(blood_group=blood_group_name).first()
        if blood_type:
            blood_type.units += quantity
        else:
            new_blood_type = BloodDatabase(blood_group=blood_group_name, units=quantity)
            db.session.add(new_blood_type)

        db.session.commit()
        return {'message': f'Inventory updated successfully for {blood_group_name}'}
    

@inventory_ns.route('/<string:id>')
@inventory_ns.response(404,"Blood inventory not found")
class InventoryFetch(Resource):
    @inventory_ns.marshal_with(inventory_model)
    @token_required
    def get(self,id):
        if id not in Blood_groups:
            return {'message':f'Invalid blood group . Please select from {Blood_groups}'},400
        blood_details = BloodDatabase.query.filter(BloodDatabase.blood_group == id).first()
        print("blood_details",blood_details)
        if blood_details is not None:
            return blood_details,201
        else:            
            return {"message":f"Blood units not available for this {id} group"},404

    @inventory_ns.marshal_with(admin_model)
    @inventory_ns.expect(inventory_model)
    @token_required
    def put(self,id):
        if not is_admin_or_donor_manager():
            return {'message': 'Admin access required'}, 403
        data = inventory_ns.payload
        blood_details = BloodDatabase.query.filter(BloodDatabase.blood_group == id).first()
        if blood_details not in Blood_groups:
            return {'message':f'Invalid blood group . Please select from {Blood_groups}'},400
        if blood_details:
            blood_details.blood_group = data['blood_group']
            blood_details.units = data['units']
            db.session.commit()
            return {"message" : f"Inventory blood group details for {blood_details.blood_group} and units {blood_details.units} successfully updated"} ,201
        else:
            return {"message":f"Blood units not found for this {id}"},404

