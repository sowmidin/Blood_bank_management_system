from flask_restx import Namespace,Resource,fields
from app import db
from app.models import Donor
from .permissions import is_admin_or_donor_manager
from app.utils import token_required

donor_ns = Namespace('donors',description="Donor management")

Blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
donor_model = donor_ns.model('Donor',{
    'id':fields.Integer(readOnly = True),
    'name':fields.String(required = True,description="Donor name"),
    'age':fields.Integer(required=True),
    'blood_group':fields.String(required=True),
    'email_id':fields.String(required=True)
})

admin_model = donor_ns.model('Admin',{
    "message":fields.String(required=True)

})

donation_model = donor_ns.model('Donation', {
    'donor_id': fields.Integer(required=True, description='ID of the donor'),
    'units_donated': fields.Integer(required=True, description='Number of units donated')
})


@donor_ns.route('/')
class DonorList(Resource):
    @token_required
    @donor_ns.marshal_with(donor_model)
    def get(self):
        return Donor.query.all()
    
    @donor_ns.expect(donor_model)
    @donor_ns.marshal_with(admin_model,code=201)
    @token_required
    def post(self):
        data = donor_ns.payload
        blood_grp = data['blood_group']
        if blood_grp not in Blood_groups:
            return {'message':f'Invalid blood group . Please select from {Blood_groups}'},400
        new_donor = Donor(name=data['name'],age=data['age'],blood_group = data['blood_group'],email_id=data['email_id']) 
        db.session.add(new_donor)
        db.session.commit()
        return {'message' : f'Donor details created for {new_donor.name}'},201
    

@donor_ns.route('/<int:id>')
@donor_ns.response(404,'Donor not found')
class DonorFetchId(Resource):
    @token_required
    @donor_ns.marshal_with(donor_model)
    def get(self,id):
        donor_name = Donor.query.get_or_404(id)
        return donor_name
    
    @donor_ns.expect(donor_model)
    @donor_ns.marshal_with(admin_model)
    @token_required
    def put(self,id):
        if not is_admin_or_donor_manager():
            print("not a aadmin")
            return {'message': 'Admin access required'}, 403
        donor_name = Donor.query.get_or_404(id)
        data = donor_ns.payload
        donor_name.name = data["name"]
        donor_name.age = data["age"]
        donor_name.blood_group = data["blood_group"]
        db.session.commit()
        return {"message":f"Donor details has been updated successfully for {donor_name.name}"},200
    
    @donor_ns.response(204,"Donor is deleted")
    @token_required
    def delete(self,id):
        if not is_admin_or_donor_manager():
            return {'message': 'Admin access required'}, 403
        donor_name = Donor.query.get_or_404(id)
        db.session.delete(donor_name)
        db.session.commit()
        return '',204
    


           