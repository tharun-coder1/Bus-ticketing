from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import time
from datetime import date
import datetime
import datetime

global uname, amount, travel_date, bid

def AddRoutes(request):
    if request.method == 'GET':
       return render(request, 'AddRoutes.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})     

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def Chat(request):
    if request.method == 'GET':
       return render(request, 'Chat.html', {})

def Faq(request):
    if request.method == 'GET':
       return render(request, 'Faq.html', {})


def AdminLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'AdminLogin.html', context)        

def getAvailable(bid, travel_date):
    available = 0
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select sum(num_seats) FROM booking where bus_id='"+str(bid)+"' and travel_date="+travel_date+" and status='Booked'")
        rows = cur.fetchall()
        for row in rows:
            available = row[0]
    if available is None:
        available = 0
    return available

def CancelBooking(request):
    if request.method == 'GET':
        bid = request.GET['bookid']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "delete from booking where booking_id = '"+str(bid)+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':"Booking Cancelled"}
        return render(request, 'UserScreen.html', context)
    

def ViewPastBookings(request):
    if request.method == 'GET':
        global uname
        today = date.today()
        font = '<font size="" color="black">'
        columns = ['Booking ID','Bus ID','Username','Booking Date','Travel Date', 'Total Seats Booked', 'Amount', 'Status', 'Cancel Now']
        output = "<table border=1 align=center class=table table-striped >"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"    
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM booking where username='"+uname+"' and travel_date > NOW()")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td>'+font+str(row[0])+'</td>'
                output+='<td>'+font+str(row[1])+'</td>'
                output+='<td>'+font+str(row[2])+'</td>'
                output+='<td>'+font+str(row[3])+'</td>'
                output+='<td>'+font+str(row[4])+'</td>'
                output+='<td>'+font+str(row[5])+'</td>'
                output+='<td>'+font+str(row[6])+'</td>'
                output+='<td>'+font+str(row[7])+'</td>'
                output+='<td><a href=\'CancelBooking?bookid='+str(row[0])+'\'><font size=3 color=black>Click Here to Cancel</font></a></td></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM booking where username='"+uname+"' and travel_date <= NOW()")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td>'+font+str(row[0])+'</td>'
                output+='<td>'+font+str(row[1])+'</td>'
                output+='<td>'+font+str(row[2])+'</td>'
                output+='<td>'+font+str(row[3])+'</td>'
                output+='<td>'+font+str(row[4])+'</td>'
                output+='<td>'+font+str(row[5])+'</td>'
                output+='<td>'+font+str(row[6])+'</td>'
                output+='<td>'+font+str(row[7])+'</td>'
                output+='<td>'+font+'Past Booking Cannot Cancel</td></tr>'

        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def ViewBookings(request):
    if request.method == 'GET':
        font = '<font size="" color="black">'
        columns = ['Booking ID','Bus ID','Username','Booking Date','Travel Date', 'Total Seats Booked', 'Amount', 'Status']
        output = "<table border=1 align=center class=table table-striped>"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"    
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM booking")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td>'+font+str(row[0])+'</td>'
                output+='<td>'+font+str(row[1])+'</td>'
                output+='<td>'+font+str(row[2])+'</td>'
                output+='<td>'+font+str(row[3])+'</td>'
                output+='<td>'+font+str(row[4])+'</td>'
                output+='<td>'+font+str(row[5])+'</td>'
                output+='<td>'+font+str(row[6])+'</td>'
                output+='<td>'+font+str(row[7])+'</td>'
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

def BookSeatAction(request):
    if request.method == 'POST':
        global travel_date, amount, bid, uname
        seats = request.POST.get('t1', False)
        tot = amount * float(seats)
        today = date.today()

        book_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(booking_id) FROM booking")
            rows = cur.fetchall()
            for row in rows:
                book_id = row[0]
        if book_id is not None:
            book_id = book_id + 1
        else:
            book_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO booking(booking_id,bus_id,username,booking_date,travel_date,num_seats,amount,status) VALUES('"+str(book_id)+"','"+str(bid)+"','"+uname+"','"+str(today)+"',"+travel_date+",'"+seats+"','"+str(tot)+"','Booked')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Your Booking Confirmed with Booking ID : '+str(book_id)
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
        

def BookSeat(request):
    if request.method == 'GET':
        global travel_date, amount, bid
        bid = request.GET['bid']
        amount = request.GET['amount']
        amount = float(amount)
        output = '<tr><td><font size="" color="black">Total&nbsp;Seats</b></td>'
        output += '<td><select name="t1">'
        for i in range(1,11):
            output += '<option values="'+str(i)+'">'+str(i)+'</option>'
        output += "</select></td></tr>"
        context= {'data1':output}
        return render(request, 'BookSeat.html', context)
            

def SearchBusesAction(request):
    if request.method == 'POST':
        global travel_date
        src = request.POST.get('t1', False)
        dest = request.POST.get('t2', False)
        travel_date = request.POST.get('t3', False)
        travel_date = str(datetime.datetime.strptime(travel_date.strip(), "%Y-%m-%d").strftime("'%Y-%m-%d'"))
        font = '<font size="" color="black">'
        columns = ['Bus ID','Bus Name','Source Place','Destination Place','Bus Fare', 'Seating Capacity', 'Visiting Stops', 'Available Seats', 'Book Now']
        output = "<table border=1 align=center class=table table-striped>"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"    
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addroutes where source='"+src+"' and destination='"+dest+"'")
            rows = cur.fetchall()
            for row in rows:
                bid = row[0]
                bname = row[1]
                src = row[2]
                des = row[3]
                fare = row[4]
                capacity = row[5]
                stops = row[6]
                available = getAvailable(bid, travel_date)
                if (capacity - available) > 0:
                    output+='<tr><td>'+font+str(bid)+'</td>'
                    output+='<td>'+font+str(bname)+'</td>'
                    output+='<td>'+font+str(src)+'</td>'
                    output+='<td>'+font+str(des)+'</td>'
                    output+='<td>'+font+str(fare)+'</td>'
                    output+='<td>'+font+str(capacity)+'</td>'
                    output+='<td>'+font+str(stops)+'</td>'
                    output+='<td>'+font+str(capacity - available)+'</td>'
                    #output+='<td>'+font+str(row[8])+'</td>'
                    output+='<td><a href=\'BookSeat?bid='+str(bid)+'&amount='+str(fare)+'\'><font size=3 color=black>Book</font></a></td></tr>'
        context= {'data':output}
        return render(request, 'UserScreen.html', context)                  


def SearchBuses(request):
    if request.method == 'GET':
        font = '<font size="" color="black">'
        output = '<table border=1 align=center class=table table-striped><tr><td><font size="" color="black">Source&nbsp;Place</b></td>'
        output += '<td><select name="t1">'
        src = []
        dest = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select source,destination FROM addroutes")
            rows = cur.fetchall()
            for row in rows:
                src.append(row[0])
                dest.append(row[1])
        for i in range(len(src)):
            output += '<option values="'+src[i]+'">'+src[i]+'</option>'
        output += "</select></td></tr>"
        output += '<tr><td><font size="" color="black">Destination&nbsp;Place</b></td>'
        output += '<td><select name="t2">'
        for i in range(len(dest)):
            output += '<option values="'+dest[i]+'">'+dest[i]+'</option>'
        context= {'data1':output}
        return render(request, 'SearchBuses.html', context)        


def UserLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+uname}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'UserLogin.html', context)

def AddRoutesAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        source = request.POST.get('t2', False)
        destination = request.POST.get('t3', False)
        fare = request.POST.get('t4', False)
        capacity = request.POST.get('t5', False)
        stops = request.POST.get('t6', False)
        bid = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(bus_id) FROM addroutes")
            rows = cur.fetchall()
            for row in rows:
                bid = row[0]
        if bid is not None:
            bid = bid + 1
        else:
            bid = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addroutes(bus_id,bus_name,source,destination,bus_fare,seating_capacity,visiting_stops) VALUES('"+str(bid)+"','"+name+"','"+source+"','"+destination+"','"+fare+"','"+capacity+"','"+stops+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Routes Details Addess with Bus ID : '+str(bid)
        context= {'data':output}
        return render(request, 'AddRoutes.html', context)
        

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BusBooking',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,gender,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+gender+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup Process Completed'
        context= {'data':output}
        return render(request, 'Signup.html', context)
      


