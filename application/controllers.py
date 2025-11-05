from flask import Flask,render_template,redirect,request, flash, url_for


# from flask_login import current_user
from datetime import datetime, timezone

from flask import current_app as app     #it refers to the app object that is created

from .models import *   #both resides in same folder so we use . 

#import to create Graph
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # this is used so that chart is created in the context of our app and it does not break the loop of our application


@app.route("/",methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        this_user = User.query.filter_by(email=email).first() #LHS attribute name in table, RHS is data fetched from database
        if this_user:
            if this_user.password == password: #check if user password is same as in database
                if this_user.type == "admin":
                    return redirect("/admin_dashboard")  # LHS name is jinja variable and RHS name is data variable that we fetched from form
                else:
                    return redirect(url_for("user_dashboard", user_id=this_user.id))
            else:
                return "Incorrect password"
        else:
            return "User does not exist"        
                
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        this_user = User.query.filter_by(email=email).first()  #if email aready exists in database
        if this_user:
            return "User already exists"
        else:
            new_user = User(fullname=name,email=email,password=password,address=address,pincode=pincode)  #entering new user to database
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")

    return render_template("signup.html")


@app.route("/newlot", methods=["GET","POST"])
def newlot():
    if request.method == 'POST':
        location = request.form.get("location")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        price = request.form.get("price")
        maxspot = int(request.form.get("maxspot"))

        # Creating Parking Lot
        newlot = Parkinglot(location=location, address=address, pincode=pincode, price_per_hour=price, total_slots=maxspot)
        db.session.add(newlot)
        db.session.commit() 

        # Creating Parking Spot 
        for i in range(1, maxspot + 1):
            spot = Parkingspot(
            spot_number=f"{newlot.lotid}-{i}",
            lotid=newlot.lotid
            )
            db.session.add(spot)

        db.session.commit()

        return redirect("/admin_dashboard")
    return render_template("newlot.html")

@app.route("/admin_dashboard", methods=['GET'])
def admin_dashboard():
    parking_data = Parkinglot.query.all()

    return render_template("admin_dashboard.html",parking_data=parking_data)


@app.route("/viewstatus/<int:lotid>",methods=['GET','POST'])
def viewstatus(lotid):
    # users = User.query.all()
    details = Parkingspot.query.filter_by(lotid=lotid).all()
    lot= Parkinglot.query.filter_by(lotid=lotid).first()

    return render_template("view.html", details=details, lot=lot)


# for displaying registered user to admin
@app.route("/regusers", methods=['GET'])
def regusers():
    users=User.query.all()

    return render_template("registered_users.html", users=users)


@app.route("/user_dashboard/<int:user_id>", methods=['GET', 'POST'])
def user_dashboard(user_id):
    users = User.query.get(user_id)
    plot = Parkinglot.query.all()
    
    user_spots = Parkingspot.query.filter_by(user_id=user_id).all()

    return render_template(
        "user_dashboard.html",
        users=users,
        plot=plot,
        user_spots=user_spots
    )

# @app.route("/delete/<int:lotid>", methods=['GET','POST'])
# def delete(lotid):
#     id = Parkinglot.query.filter_by(lotid=lotid).first()
#     occupied_spot = Parkingspot.query.filter_by(lotid=lotid, status="available").first()
#     if occupied_spot:
#         db.session.delete(id)
#         db.session.commit()
#         return redirect("/admin_dashboard")
#     else:
#         flash("Cannot Delete, Some Spots are Occupied.")        # Error might occur see this
#         return redirect("/admin_dashboard")

@app.route("/delete/<int:lotid>", methods=['GET', 'POST'])
def delete(lotid):
    lot = Parkinglot.query.filter_by(lotid=lotid).first()
    
    occupied_spot = Parkingspot.query.filter_by(lotid=lotid, status="occupied").first()


    if occupied_spot:
        flash("Cannot delete. Some spots in this lot are currently occupied.")
        return redirect("/admin_dashboard")
    else:
        # First delete all the spots related to the lot
        Parkingspot.query.filter_by(lotid=lotid).delete()
        # Then delete the lot itself
        db.session.delete(lot)
        db.session.commit()
        flash("Lot and its spots deleted successfully.")
        return redirect("/admin_dashboard")



@app.route("/book_spot/<int:lotid>/<int:user_id>", methods=['GET','POST'])
def book_spot(lotid, user_id):
    lot = Parkinglot.query.get(lotid)
    this_user = User.query.get(user_id)

    spot = Parkingspot.query.filter_by(lotid=lotid, status="available").first()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # current time
    
    if request.method == "POST":
        # Mark spot as booked 
        vehno = request.form.get("vno")
        spot.vehicle_No = vehno
        spot.status = "occupied"
        spot.parked_at = datetime.now() 
        spot.user_id = user_id 
        lot.total_slots -= 1
        db.session.commit()
        return redirect(url_for("user_dashboard", user_id=this_user.id))
    return render_template("bookslot.html", lot=lot, this_user=this_user, spot=spot, datetime=current_time)

    
@app.route("/release/<int:spot_id>", methods=['GET','POST'])
def release(spot_id):
    spot = Parkingspot.query.get(spot_id)

    if request.method == "POST":
        release_time = datetime.now()
        spot.released_at = release_time
        spot.status = "released"

        # Fetch associated parking lot
        lot = Parkinglot.query.get(spot.lotid)
        if lot:
            lot.total_slots += 1  # Increase available slot

        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=spot.user_id))

    this_user = spot.user
    release_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    return render_template("release.html",spot=spot,this_user=this_user, release_time=release_time)



@app.route("/deletespot/<int:spot_id>", methods=['GET','POST'])
def deletespot(spot_id):
    spot = Parkingspot.query.get(spot_id)

    if spot.status != "available":
        flash("Cannot delete: Spot is currently occupied")
        return redirect(url_for("admin_dashboard"))
    
    parkinglot = spot.parkinglot
    if parkinglot.total_slots > 0:
        parkinglot.total_slots -= 1

    db.session.delete(spot)
    db.session.commit()
    flash("Spot deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


#edit lot
@app.route("/editlot/<int:lotid>", methods=["GET", "POST"])
def editlot(lotid):
    lot = Parkinglot.query.get_or_404(lotid)

    if request.method == 'POST':
        lot.location = request.form["location"]
        lot.address = request.form["address"]
        lot.pincode = int(request.form["pincode"])
        lot.price_per_hour = float(request.form["priceperhour"])
        new_total = int(request.form["maxspot"])
        old_total = lot.total_slots

        lot.total_slots = new_total

        # Update Parkingspot entries
        if new_total > old_total:
            for i in range(old_total + 1, new_total + 1):
                new_spot = Parkingspot(
                    spot_number=i,
                    status='available',
                    lotid=lotid
                )
                db.session.add(new_spot)

        elif new_total < old_total:
            # Delete extra spots (those with highest spot_number)
            extra_spots = Parkingspot.query.filter_by(lotid=lotid).order_by(Parkingspot.spot_number.desc()).limit(old_total - new_total).all()
            for spot in extra_spots:
                db.session.delete(spot)

        try:
            db.session.commit()
            flash("Parking lot and spots updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating: {str(e)}", "danger")

        return redirect(url_for("admin_dashboard"))

    return render_template("editlot.html", lot=lot)






# Summary
@app.route("/summary")
def summary():
    lots = Parkinglot.query.all()
    charts = []  # List to hold chart file names for each lot

    for lot in lots:
        lot_spots = Parkingspot.query.filter_by(lotid=lot.lotid).all()
        occupied = sum(1 for spot in lot_spots if spot.status == "occupied")
        available = sum(1 for spot in lot_spots if spot.status == "available")

        labels = ["Occupied", "Available"]
        sizes = [occupied, available]
        colors = ["red", "green"]

        plt.figure()  # Start a new figure
        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%")
        plt.title(f"Lot {lot.lotid} - {lot.location}")
        filename = f"static/pie_lot_{lot.lotid}.png"
        plt.savefig(filename)
        plt.close()

        charts.append({
            "lot_name": lot.location,
            "filename": filename
        })

    return render_template("summary.html", charts=charts)


@app.route("/user_summary/<int:user_id>")
def user_summary(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    # Get all parking spots used by this user
    user_spots = Parkingspot.query.filter_by(user_id=user_id).all()

    # Count occupied and released statuses
    occupied = sum(1 for spot in user_spots if spot.status == "occupied")
    released = sum(1 for spot in user_spots if spot.status == "released")

    if occupied + released == 0:
        chart_filename = None  # no need to generate a chart
    else:
        # Generate pie chart
        labels = ['Occupied', 'Released']
        sizes = [occupied, released]
        colors = ['red', 'yellow']

        import matplotlib.pyplot as plt
        plt.figure()
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.title(f"Parking Spot Summary for {user.fullname}")

        chart_filename = f"static/user_{user_id}_summary.png"
        plt.savefig(chart_filename)
        plt.close()

    return render_template("user_summary.html", user=user, chart_filename=chart_filename)

    


