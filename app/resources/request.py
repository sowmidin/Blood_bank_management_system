from flask_restx import Namespace,Resource,fields
from app import db
from app.models import Donor,BloodDatabase
from app.utils import token_required
from flask import request

blood_request_ns = Namespace('blood_request',description="Blood Unit Requests")

blood_request_model = blood_request_ns.model('Request',{
    'blood_type':fields.String(required=True,description="Request blood group"),
    'units_needed':fields.Integer(required=True)

})

@blood_request_ns.route('/')
class BloodRequest(Resource):
    @blood_request_ns.expect(blood_request_model)
    #@blood_request_ns.marshal_with(blood_request_model)
    @token_required
    def post(self):
        data = blood_request_ns.payload
        blood_request_type = data['blood_type']
        units_needed = data['units_needed']
        blood_data = BloodDatabase.query.filter(BloodDatabase.blood_group == blood_request_type).first()
        print(f"blood data",blood_data)
        if blood_data and units_needed <= blood_data.units :
            print(f"Blood units are purchased for this type {blood_data}")
            units_remaining = blood_data.units - units_needed
            blood_data.units = units_remaining
            db.session.commit()
            return {"message": f"Blood requests for {blood_request_type} - {units_needed} units purchased successfully"}
        
        elif blood_data  and units_needed > blood_data.units:
            purchased_units = blood_data.units
            units_remaining = 0
            blood_data.units = units_remaining
            db.session.commit()            
            msg = f"The blood units are less compared to units needed . The purchased units for this blood type{blood_request_type} - {purchased_units} units . The donor details for this blood type {blood_request_type} is there . Please contact for blood request"
            donor_details = Donor.query.filter(Donor.blood_group == blood_request_type).first()
            print("donor details",donor_details)
            print({"msg":f"{donor_details}"})
            if donor_details:
                return {"message": f" {msg} {donor_details.name} , {donor_details.blood_group},{donor_details.email_id}"}
            else:
                return {"message":msg}
        else:
            print(f"No sufficient blood units available")
            donor_details = Donor.query.filter(Donor.blood_group == blood_request_type).all()
            if donor_details:
                msg = f"There is no blood units for this  {blood_request_type} The donor details for this blood type {blood_request_type} is there . Please contact for blood request"
                return {"message" : f"{msg} {donor_details.name} , {donor_details.blood_group},{donor_details.email_id}"}  
            else:
                return {"message": "No blood units are available . no blood Donors are also available"}          

            

            



