from flask import Blueprint, redirect, request, url_for, render_template
from .models import AgencyLog, AgencyMast, Location, Supervisor, WorkType, ToolLog
from . import db    
from .cust_functions import *
from datetime import datetime

agencyapp = Blueprint('agencyapp', __name__)



@agencyapp.route('/agency')
def agency_main():
    date = datetime.now().date()
    time = (datetime.now().time()).strftime("%H:%M")
    log = AgencyLog.query.filter_by(date=date).all()
    supervisors = Supervisor.query.all()
    worktypes = WorkType.query.all()
    agencies = AgencyMast.query.all()
    locations = Location.query.all()
    return render_template('Agency/agency.html', log=log, supervisors=supervisors,
                            worktypes=worktypes, agencies=agencies, 
                            locations=locations, date=date, time=time)



@agencyapp.route('/addagency', methods=['POST'])
def add_log():
    if request.form:
        a = ''
        wt = ''
        sup = ''
        loc = ''
        order_no = request.form.get('orderno')
        agency_name = request.form.get('agencyname').upper()
        total = request.form.get('totalpeople')
        worktyp = request.form.get('worktype')
        represent = request.form.get('rprname')
        vehicle = request.form.get('ifvehicle')
        remark = request.form.get('remark')
        supervisor = request.form.get('supervisor').upper()
        location = request.form.get('location').upper()
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
    agency_mast = AgencyMast.query.all()
    if request.form:
        al_id = int(request.form.get('al_id'))
        log_item = AgencyLog.query.get(al_id)
        db.session.delete(log_item)
        db.session.commit()
        return redirect(url_for('agencyapp.report_agency'))
    return render_template('Reports/report-agency.html', log=log,
                            locations=locations, agency_mast=agency_mast)



@agencyapp.route('/printAgencyReport', methods=['POST'])
def print_agency_report():

    if request.form:
        printid = int(request.form.get('printid'))
        date = request.form.get('date')
        if date:
            date =  datetime.strptime(date, '%Y-%m-%d').date()

        if printid == 1:
            title = 'Agency Records'
            logs = AgencyLog.query.filter_by(date=date).all()
            count = len(logs)
            extras = 0
            for i in logs:
                if i.manpower:
                    a = i.manpower
                    extras+=a

            return render_template('Reports/agency-report-print.html', logs=logs, title=title,
                                    date=date, count=count, extras=extras)
        elif printid == 2:
            check = request.form.get('deptcheck')
            loc = request.form.get('loc')
            if check:
                title = 'Agency Records Sorted by Location'
                logs = AgencyLog.query.filter_by(date=date).all()
            else:
                title = 'Agency Report By Location'
                if date:
                    logs = AgencyLog.query.filter(AgencyLog.date==date, AgencyLog.location_id==loc).all()
                else:
                    loc_logs = Location.query.get(loc)
                    logs = loc_logs.log
                

            count = len(logs)
            extras = 0
            for i in logs:
                if i.manpower:
                    a = i.manpower
                    extras+=a
            return render_template('Reports/agency-report-print.html', logs=logs, title=title,
                                    date=date, count=count, extras=extras)
        elif printid == 3:
            agency_id = request.form.get('agency_name')

            if agency_id:
                agency_id = int(agency_id)
                agency_log = AgencyMast.query.get(agency_id)
                logs = agency_log.log
                count = len(logs)
                extras = 0
                for i in logs:
                    if i.manpower:
                        extras += i.manpower
                title = 'Agency Report'
                return render_template('Reports/agency-report-print.html', logs=logs, title=title,
                                        count=count, extras=extras)






@agencyapp.route('/freqAgency')
def freq_visitor():

    agency_all = AgencyMast.query.all()
    log = []
    for i in agency_all:
        a = len(i.log)
        log.append([i.agency_name,a])
    return render_template('Reports/report-agency-freq.html', log=log) 

@agencyapp.route('/LocationAgency')
def loc_agency():
    location_all = Location.query.all()

    if request.form:
        loc_id = int(request.form.get('loc'))
        loc = Location.query.get(loc_id)
        logs = loc.log
        return render_template('')

@agencyapp.route('/agencytools', methods=['GET', 'POST'])
def tools_agency():
    today = datetime.now().date()
    log = AgencyLog.query.filter_by(date=today).all()
    tools = ToolLog.query.all()
    if request.form:
        agency_log_id = int(request.form.get('tool_logid'))
        tool = request.form.get('tool_text')

        a_log = AgencyLog.query.get(agency_log_id)
        a_log.add_tool(tool_name=tool)
        return redirect(url_for('agencyapp.tools_agency'))
    return render_template('Agency/agency-tools.html', log=log, tools=tools)

@agencyapp.route('/editagency', methods=['GET', 'POST'])
def edit_agency():
    date = request.form.get('selected_date')
    if date:
        date = datetime.strptime(date, '%Y-%M-%d').date()
    log = AgencyLog.query.filter_by(date=date).all()
    return render_template('Agency/edit-agency.html', log=log, date=date)

@agencyapp.route('/changedata', methods=['POST'])
def chnage_data():
    if request.form:
        log_id = request.form['logid']
        orderno = request.form['order']
        name = request.form['name']
        workers = request.form['workers']
        in_time = request.form['in_time']
        out_time = request.form['out_time']

        if log_id:
            log_id = int(log_id)
            log_item = AgencyLog.query.get(log_id)

        if in_time:
            in_time = datetime.strptime(in_time, '%H:%M').time()
            log_item.in_time = in_time
            db.session.commit()

        if out_time:
            out_time = datetime.strptime(out_time, '%H:%M').time()
            log_item.out_time = out_time
            db.session.commit() 
        if workers:
            workers = int(workers)
            log_item.manpower = workers
            db.session.commit()
        
        if name:
            log_item.name = name
            db.session.commit()
        print(f'{orderno}, {name}, {workers}, {in_time}, {out_time}')
    return {'status':'okay'}

