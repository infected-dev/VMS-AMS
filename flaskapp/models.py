from . import db
from flask_login import UserMixin
from flaskapp import app

class Location(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'location'

    lid = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20), unique=True)
    log = db.relationship('AgencyLog', backref='locationm', lazy=True)

    def __init__(self, location_name):
        self.location_name = location_name.upper()

    def check_location(name):
        loc = Location.query.filter_by(location_name=name).first()
        return loc

    def add_location(location_name):
        loc = Location(location_name=location_name)
        db.session.add(loc)
        db.session.commit()

    def del_location(location_id):
        loc = Location.query.get(location_id)
        db.session.delete(loc)
        db.session.commit()


class Supervisor(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'supervisor'

    sid = db.Column(db.Integer, primary_key=True)
    supervisor_name = db.Column(db.String(25))
    log = db.relationship('AgencyLog', backref='superm', lazy=True)

    def __init__(self, supervisor_name):
        self.supervisor_name = supervisor_name.upper()
    
    def check_supervisor(name):
        supvisor = Supervisor.query.filter_by(supervisor_name=name).first()
        return supvisor

    def add_supervisor(supervisor_name):
        supvisor = Supervisor(supervisor_name=supervisor_name)
        db.session.add(supvisor)
        db.session.commit()

    def del_supervisor( id):
        supvisor = Supervisor.query.get(id)
        db.session.delete(supvisor)
        db.session.commit()
        


class AgencyMast(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'agencymast'

    a_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String(50), unique=True)
    log = db.relationship('AgencyLog', backref='agenm', lazy=True)

    def __init__(self, agency_name):
        self.agency_name = agency_name.upper()

    def check_agency( name):
        agen = AgencyMast.query.filter_by(agency_name=name).first()
        return agen

    def add_agency(name):
        agen = AgencyMast(agency_name=name)
        db.session.add(agen)
        db.session.commit()

    def del_agency( id):
        agen = AgencyMast.get(id)
        db.session.delete(agen)
        db.session.commit()

class WorkType(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'worktype'

    wt_id = db.Column(db.Integer, primary_key=True)
    work_type = db.Column(db.String(30))
    log = db.relationship('AgencyLog', backref='wtyp', lazy=True)

    def __init__(self, work_type):
        self.work_type = work_type.upper()

    def check_work( wtype):
        wtyp = WorkType.query.filter_by(work_type=wtype).first()
        return wtyp

    def add_wtype(wtype):
        wtyp = WorkType(work_type=wtype)
        db.session.add(wtyp)
        db.session.commit()

    def del_wtype(id):
        wtyp = WorkType.get(id)
        db.session.delete(wtyp) 
        db.session.commit()

class ToolMast(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'toolmast'

    tool_id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(30), unique=True)
    logs = db.relationship('Tool_log', backref='tool', lazy=True)

    def __init__(self, tool_name):
        self.tool_name = tool_name

    def checktool_add(tool_name):
        var = ToolMast.query.filter_by(tool_name=tool_name).first()
        if var:
            return {'status':'already exists'}
        else:
            var = ToolMast(tool_name=tool_name)
            db.session.add(var)
            db.session.commit()
            return {'status':'ok'}


    def addtool(self, agency_id):
        toolog = Tool_log(tool_id=self.tool_id, agency_log=agency_id)
        db.session.add(toolog)
        db.session.commit()


class Tool_log(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'tool_log'

    toolog_id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('toolmast.tool_id'))
    agency_log = db.Column(db.Integer, db.ForeignKey('agencylog.al_id'))



class AgencyLog(db.Model):
    __bind_key__ = 'agency'
    __tablename__ = 'agencylog'

    al_id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(30))
    agency_id = db.Column(db.Integer, db.ForeignKey('agencymast.a_id'))
    worktype_id = db.Column(db.Integer, db.ForeignKey('worktype.wt_id'))
    contact_person = db.Column(db.String(30))
    manpower = db.Column(db.Integer)
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(12))
    vehicle_no = db.Column(db.String(15))
    remarks = db.Column(db.Integer)
    Supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.sid'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.lid'))
    tools = db.relationship('Tool_log', backref='tools', lazy=True)

    def __init__(self, order, agency_id, worktype_id, contact_person, manpower, date, in_time, vehicle_no, remarks, Supervisor_id, location_id):
        self.order = order
        self.agency_id = agency_id
        self.worktype_id = worktype_id
        self.contact_person = contact_person.upper()
        self.manpower = manpower
        self.date = date
        self.in_time = in_time
        self.vehicle_no = vehicle_no
        self.remarks = remarks
        self.Supervisor_id = Supervisor_id
        self.location_id = location_id

    

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    VeEntryDate = db.Column(db.Date)
    VeID = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    VeNO = db.Column(db.String(25), nullable=False)
    VendorName = db.Column(db.String(80))
    visited_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    VehicleTypeName_id = db.Column(
        db.Integer, db.ForeignKey('vehicletypes.id'))
    InTime = db.Column(db.Time)
    OutTime = db.Column(db.Time)
    TotalDuration = db.Column(db.String(25))


class VehicleTypes(db.Model):
    __tablename__ = "vehicletypes"

    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(10))
    vehicles = db.relationship('Vehicle', backref='vehicle_type')
    compnay_vehicles = db.relationship('CompanyVehicle', backref='comp_vehicle_type')


class CompanyVehicle(db.Model):
    __tablename__ = "companyvehicles"

    id = db.Column(db.Integer, primary_key=True)
    comp_vehicle_no = db.Column(db.String(20), unique=True)
    vehicle_type = db.Column(db.Integer, db.ForeignKey('vehicletypes.id'))
    model_name = db.Column(db.String(20))
    timesheet = db.relationship('CompanyTimesheet', backref='comp_timesheet')


class CompanyTimesheet(db.Model):
    __tablename__ = 'companyvehiclestime'

    id = db.Column(db.Integer, primary_key=True)
    comp_vehicle_id = db.Column(db.Integer, db.ForeignKey('companyvehicles.id'))
    visited_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    date = db.Column(db.Date)
    InTime = db.Column(db.Time)
    OutTime = db.Column(db.Time)
    duration = db.Column(db.String(25)) 


class Visitor(db.Model):
    __tablename__ = 'visitor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    contact = db.Column(db.String(11))
    place_from = db.Column(db.String(20))
    activities = db.relationship('Activity', backref='activity')
    a_timesheet = db.relationship('Timesheet_Visitor', backref="a_timelog")

   
class Activity(db.Model):
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    visiting_purpose = db.Column(db.String(50))
    visiting_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))
    visiting_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    timelog = db.relationship('Timesheet_Visitor',backref='active')
   

class Timesheet_Visitor(db.Model):
    __tablename__ = 'timesheet_visitor'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    extras = db.Column(db.Integer, default=0)
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))
    


class Department(db.Model):
    __tablename__ = "department"
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    employees = db.relationship('Employee', backref='dept')
    activity_dept = db.relationship('Activity',  backref='visited_dept')
    outside_vehicles = db.relationship('Vehicle', backref='outside_dept')
    mill_vehicles = db.relationship('CompanyTimesheet', backref='mill_dept')


class Employee(db.Model):
    __tablename__ = "employee"
    
    id = db.Column(db.Integer, primary_key=True)
    employee_name =  db.Column(db.String(80), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    activity_emp = db.relationship('Activity' , backref='visited_employee')


class User(UserMixin ,db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(13))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def user_role(self):
        return self.role_id


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='current_role')

