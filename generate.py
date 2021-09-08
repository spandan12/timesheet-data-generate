import random
import datetime
import csv  
import math

# employee ranging from id number 1 to 30
employee_range = range(1, 30, 1)

# department id ranging from 1 to 5
department_start_id = 1
department_end_id = 5

# punch apply date range
punch_apply_date_start = datetime.date(2021, 6, 23)
punch_apply_date_end = datetime.date(2021, 7, 23)

# increment for punch apply date
delta = datetime.timedelta(days=1)

# open file and add headers to the csv file
f = open('./dataset.csv', 'w')
writer = csv.writer(f)
writer.writerow(['employee_id', 'cost_center', 'punch_in_time', 'punch_out_time', 'punch_apply_date', 'hours_worked', 'paycode'])

# randomly map employee to department
employee_department_mapping = {}
for employee_id in employee_range:
    department_id = random.randint(department_start_id, department_end_id)
    employee_department_mapping[employee_id] = department_id

# Generate data for all the punch apply dates
while punch_apply_date_start <= punch_apply_date_end:
    # Generate data for all the employees
    
    is_weekend = punch_apply_date_start.weekday() > 4
    worked_employee_range = random.sample(employee_range, math.floor(len(employee_range)/2))
    no_record_employees = random.sample(employee_range, 5)

    for employee_id in employee_range:
        department_id = employee_department_mapping[employee_id]

        if employee_id in no_record_employees:
            continue

        total_time_spent = 8
        absent = random.choices([1, 0], [0.3, 0.7])[0]
        if (is_weekend and employee_id not in worked_employee_range) or (absent == 1):
            print(employee_id, department_id, '', '', punch_apply_date_start, total_time_spent, 'ABSENT')
            writer.writerow([employee_id, department_id, '', '', punch_apply_date_start, total_time_spent, 'ABSENT'])
            continue
        
        total_time = 0
        
        on_call = random.choices([1, 0], [0.5, 0.5])[0]
        hours_on_call = random.randint(5, 8)
        if on_call == 1:
            print(employee_id, department_id, '', '', punch_apply_date_start, hours_on_call, 'ON_CALL')
            writer.writerow([employee_id, department_id, '', '', punch_apply_date_start, hours_on_call, 'ON_CALL'])
            total_time_spent = 8 - hours_on_call
            if total_time_spent == 0:
                continue

        # to do: make on_call and charge mutually exclusive -  done
        # make hours worked on absent =8 - done
        # lets make break time less than 1 
        # lets make no record for 5 employees in a day
        
        charge = random.choices([1, 0], [0.5, 0.5])[0]
        hours_charge = random.randint(1, 3) 
        if on_call !=1 and charge == 1:
            print(employee_id, department_id, '', '', punch_apply_date_start, hours_charge, 'CHARGE')
            writer.writerow([employee_id, department_id, '', '', punch_apply_date_start, hours_charge, 'CHARGE'])

        start_time = datetime.time(random.choices([6,14], [0.5,0.5])[0], random.randint(0,20), 0)
        punch_in_time = datetime.datetime.combine(punch_apply_date_start, start_time)

        break_time = random.randint(2, 5) if on_call != 1 else 0
        minutes_worked_interval_I = random.randint(30,50) if on_call !=1 else total_time_spent*60

        
        punch_out_time = punch_in_time + datetime.timedelta(hours=break_time, minutes=minutes_worked_interval_I)
        hours_worked = break_time + round(minutes_worked_interval_I/60, 1) 
        print(employee_id, department_id, punch_in_time, punch_out_time, punch_apply_date_start, hours_worked, 'WRK')
        writer.writerow([employee_id, department_id, punch_in_time, punch_out_time, punch_apply_date_start, hours_worked, 'WRK'])
        punch_in_time = punch_out_time

        remaining = total_time_spent* 60 - minutes_worked_interval_I - break_time * 60

        if remaining < 60:
            continue
        
        break_minutes = random.randint(30,60)
        punch_out_time = punch_in_time + datetime.timedelta(minutes=break_minutes)
        break_hour = round(break_minutes/60, 1) 
        print(employee_id, department_id, '', '', punch_apply_date_start, break_hour, 'BREAK')
        writer.writerow([employee_id, department_id, '', '', punch_apply_date_start, break_hour, 'BREAK'])
        punch_in_time = punch_out_time

        total_minutes_worked = minutes_worked_interval_I + break_minutes - 60
        total_hours_worked = break_time + 1

        remaining_minutes_left = total_time_spent* 60 - total_minutes_worked - total_hours_worked * 60
        punch_out_time = punch_in_time + datetime.timedelta(minutes=remaining_minutes_left)
        hours_worked_interval_II = round(remaining_minutes_left/60, 1) 
        print(employee_id, department_id, punch_in_time, punch_out_time, punch_apply_date_start, hours_worked_interval_II, 'WRK')
        writer.writerow([employee_id, department_id, punch_in_time, punch_out_time, punch_apply_date_start, hours_worked_interval_II, 'WRK'])



    punch_apply_date_start += delta
