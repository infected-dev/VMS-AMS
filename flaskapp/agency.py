from flask import Blueprint, redirect, request, url_for, render_template
from .models import AgencyLog, AgencyMast, Location, Supervisor, WorkType
from . import db    
from .cust_functions import *
from datetime import datetime

agencyapp = Blueprint('agencyapp', __name__)

@agencyapp.route('/agency')
def agency_main():
    log = AgencyLog.query.all()
    supervisors = Supervisor.query.all()
    worktypes = WorkType.query.all()
    agencies = AgencyMast.query.all()
    locations = Location.query.all()
    return render_template('agency.html', log=log, supervisors=supervisors,
                            worktypes=worktypes, agencies=agencies, 
                            locations=locations)

@agencyapp.route('/addagency', methods=['POST'])
def add_log():
    if request.form:
        a = ''
        wt = ''
        sup = ''
        loc = ''
        order_no = request.form.get('orderno')
        agency_name = request.form.get('agencyname')
        total = request.form.get('totalpeople')
        worktyp = request.form.get('worktype')
        represent = request.form.get('rprname')
        vehicle = request.form.get('ifvehicle')
        remark = request.form.get('remark')
        supervisor = request.form.get('supervisor')
        location = request.form.get('location')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        in_time = datetime.strptime(request.form.get('intime'), '%H:%M').time()
        out_time = request.form.get('outime')


        if AgencyMast.check_agency(name=agency_name) is None:
            a = AgencyMast(agency_name=agency_name)
            db.session.add(a)
            db.session.commit()
            a = a.a_id
        else:
            a = AgencyMast.query.filter_by(agency_name=agency_name).first()
            a = a.a_id
            


        if WorkType.check_work(wtype=worktyp) is None:
            wt = WorkType(work_type=worktyp)
            db.session.add(wt)
            db.session.commit()

            wt = wt.wt_id
        else: 
            wt = WorkType.query.filter_by(work_type=worktyp).first()
            wt = wt.wt_id
            


        if Supervisor.check_supervisor(name=supervisor) is None:
            supe = Supervisor(supervisor_name=supervisor)
            db.session.add(supe)
            db.session.commit()

            sup = supe.sid
        else:
            supe = Supervisor.query.filter_by(supervisor_name=supervisor).first()
            sup = supe.sid
            

        if Location.check_location(name=location) is None:
            loc = Location(location_name=location)
            db.session.add(loc)
            db.session.commit()

            loc = loc.lid
        else:
            loc = Location.query.filter_by(location_name=location).first()
            loc = loc.lid
        

        agency_log = AgencyLog(order=order_no, agency_id=a, worktype_id=wt,
                                contact_person=represent, manpower=total,
                                date=date, in_time=in_time,
                                vehicle_no=vehicle, remarks=remark, 
                                Supervisor_id=sup, location_id=loc)
        db.session.add(agency_log)
        db.session.commit()
        return redirect(url_for('agencyapp.agency_main'))

@agencyapp.route('/updateAgency', methods=['POST'])
def update_agency():
    if request.form:
        lid = request.form['lid']
        exit_time = datetime.strptime(
            request.form['exitime'], '%H:%M').time()
        agen_log = AgencyLog.query.get(lid)
        agen_log.out_time = exit_time
        db.session.commit()
        intime = agen_log.in_time
        outtime = agen_log.out_time
        diff = timeobj(intime, outtime)
        agen_log.duration = diff
        db.session.commit()
        return {'status': 'Success'}


@agencyapp.route('/reportAgency', methods=['GET','POST'])
def report_agency():
    log = AgencyLog.query.all()
    locations = Location.query.all()
    return render_template('report-agency.html', log=log,
                            locations=locations)

@agencyapp.route('/printAgencyReport', methods=['POST'])
def print_agency_report():
    if request.form:
        printid = int(request.form.get('printid'))
        date =  datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        if printid == 1:
            title = 'Agency Records'
            logs = AgencyLog.query.filter_by(date=date).all()
            count = len(logs)
            extras = 0
            for i in logs:
                if i.manpower:
                    a = i.manpower
                    extras+=a

            return render_template('agency-report-print.html', logs=logs, title=title,
                                    date=date, count=count, extras=extras)
        elif printid == 2:
            check = request.form.get('deptcheck')
            loc = request.form.get('loc')
            if check:
                title = 'Agency Records Sorted by Location'
                logs = AgencyLog.query.filter_by(date=date).all()
                count = len(logs)
                extras = 0
                for i in logs:
                    if i.manpower:
                        a = i.manpower
                        extras+=a
                return render_template('agency-report-print.html', logs=logs, title=title,
                                        date=date, count=count, extras=extras)