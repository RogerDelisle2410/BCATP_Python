"""Application overview

This Flask application exposes multiple routes ("tabs") for managing different
datasets (for example: `army`, `airforce`, `navy`, `bcatp`, `dewline`,
`pinetree`, `defunct`, `midcanada`, `planes`, `ships`, `tanks`). It uses
SQLAlchemy models (imported from `models.py`) and a SQLite database configured
via `SQLALCHEMY_DATABASE_URI`.

Key behaviors:
- Per-tab listing routes with optional `starts` filtering and pagination
- Per-tab `/add` endpoints that create records from `request.form`
- A universal edit route `/<tab>/edit/<id>` that updates selected fields
- A universal delete route `/delete/<tab>/<id>`
- A `global_search` route that scans all tables and computes the page for
  matches using a fixed `per_page` value (10 by default in this app)

This module-level comment is informational only and does not change runtime
behavior.
"""

from flask import Flask, render_template, request, redirect, jsonify
from models import (db,Bcatp, Army, Airforce, Navy, Dewline, Pinetree, Defunct, Midcanada, Planes, Ships, Tanks, VisitorCount, VisitorLog,)
from flask_cors import CORS
import os

# 1. Create the Flask app FIRST
app = Flask(__name__, instance_relative_config=True) 

# 2. Apply CORS AFTER app is created
CORS(
    app,
    resources={r"/*": {
        "origins": [
            "https://bcatp-python-gxepcqa3d5crbchn.canadacentral-01.azurewebsites.net",
            "https://jrd-projects-hdawd5crfdatfudg.canadacentral-01.azurewebsites.net",
            "http://localhost:5000",
            "http://127.0.0.1:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }}
) 

import requests

def lookup_location(ip):
    try:
        clean_ip = ip.split(":")[0]
        r = requests.get(f"http://ip-api.com/json/{clean_ip}", timeout=3)
        data = r.json()

        if data.get("status") == "success":
            city = data.get("city")
            country = data.get("country")
            if city and country:
                return f"{city}, {country}"
            if country:
                return country

        return "Unknown 1"
    except:
        return "Unknown 2"

# 3. Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "sqlite:///BCATPDB2.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 4. Initialize DB
db.init_app(app)

# -----------------------------
# ROOT
# -----------------------------
@app.route("/")
def index():
    return redirect("/home")


@app.route("/ping")
def ping():
    return "FLASK IS ALIVE"


# ============================================================
# UNIVERSAL EDIT ROUTE
# ============================================================
@app.route("/<tab>/edit/<int:id>", methods=["GET", "POST"])
def edit(tab, id):

    models = {
        "bcatp": Bcatp,
        "army": Army,
        "airforce": Airforce,
        "navy": Navy,
        "dewline": Dewline,
        "pinetree": Pinetree,
        "defunct": Defunct,
        "midcanada": Midcanada,
        "planes": Planes,
        "ships": Ships,
        "tanks": Tanks,
        "visitorcount": VisitorCount,
        "visitorlog": VisitorLog,
    }

    Model = models.get(tab)
    if not Model:
        return "Invalid tab", 404

    row = Model.query.get_or_404(id)

    if request.method == "POST":
        tab = request.form.get("tab", tab)

        row.name = request.form.get("name")

        # Only update long/lat if present and non-empty
        lon_val = request.form.get("longitude")
        lat_val = request.form.get("latitude")

        if lon_val not in (None, ""):
            row.longitude = float(lon_val)
        if lat_val not in (None, ""):
            row.latitude = float(lat_val)

        row.comment = request.form.get("comment")
        row.wiki = request.form.get("wiki")

        db.session.commit()
        return redirect(f"/{tab}")

    return render_template("edit.html", row=row, active_tab=tab)


# ============================================================
# HOME TAB
# ============================================================
@app.route("/home")
def home():
    return render_template("home.html", active_tab="home")


# ============================================================
# ARMY TAB
# ============================================================
@app.route("/army")
def army():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Army.query

    if starts:
        query = query.filter(Army.name.ilike(f"%{starts}%"))

    if per_page == 0:
        rows = query.order_by(Army.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Army.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "army.html",
        rows=rows,
        active_tab="army",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/army/add", methods=["POST"])
def army_add():
    new_row = Army(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/army")


# ============================================================
# BCATP TAB
# ============================================================
@app.route("/bcatp")
def bcatp():
    page = request.args.get("page", 1, type=int)
    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)
    starts = request.args.get("starts", "").strip()
    query = Bcatp.query
    if starts:
        query = query.filter(Bcatp.name.ilike(f"%{starts}%"))
    if per_page == 0:
        rows = query.order_by(Bcatp.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Bcatp.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages
    return render_template(
        "bcatp.html",
        rows=rows,
        active_tab="bcatp",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/bcatp/add", methods=["POST"])
def bcatp_add():
    new_row = Bcatp(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/bcatp")


# ============================================================
# AIR FORCE TAB
# ============================================================
@app.route("/airforce")
def airforce():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Airforce.query

    if starts:
        query = query.filter(Airforce.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Airforce.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Airforce.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "airforce.html",
        rows=rows,
        active_tab="airforce",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/airforce/add", methods=["POST"])
def airforce_add():
    new_row = Airforce(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/airforce")


# ============================================================
# NAVY TAB
# ============================================================
@app.route("/navy")
def navy():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Navy.query

    if starts:
        query = query.filter(Navy.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Navy.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Navy.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "navy.html",
        rows=rows,
        active_tab="navy",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/navy/add", methods=["POST"])
def navy_add():
    new_row = Navy(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/navy")


# ============================================================
# DEW LINE TAB
# ============================================================
@app.route("/dewline")
def dewline():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Dewline.query

    if starts:
        query = query.filter(Dewline.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Dewline.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Dewline.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "dewline.html",
        rows=rows,
        active_tab="dewline",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/dewline/add", methods=["POST"])
def dewline_add():
    new_row = Dewline(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/dewline")


# ============================================================
# PINETREE TAB
# ============================================================
@app.route("/pinetree")
def pinetree():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Pinetree.query

    if starts:
        query = query.filter(Pinetree.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Pinetree.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Pinetree.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "pinetree.html",
        rows=rows,
        active_tab="pinetree",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/pinetree/add", methods=["POST"])
def pinetree_add():
    new_row = Pinetree(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/pinetree")


# ============================================================
# DEFUNCT TAB
# ============================================================
@app.route("/defunct")
def defunct():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Defunct.query

    if starts:
        query = query.filter(Defunct.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Defunct.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Defunct.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "defunct.html",
        rows=rows,
        active_tab="defunct",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/defunct/add", methods=["POST"])
def defunct_add():
    new_row = Defunct(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/defunct")


# ============================================================
# MID CANADA TAB
# ============================================================
@app.route("/midcanada")
def midcanada():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Midcanada.query

    if starts:
        query = query.filter(Midcanada.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Midcanada.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Midcanada.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "midcanada.html",
        rows=rows,
        active_tab="midcanada",
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/midcanada/add", methods=["POST"])
def midcanada_add():
    new_row = Midcanada(
        name=request.form.get("name"),
        longitude=float(request.form.get("longitude")),
        latitude=float(request.form.get("latitude")),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/midcanada")


# ============================================================
# PLANES TAB
# ============================================================
@app.route("/planes")
def planes():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Planes.query

    if starts:
        query = query.filter(Planes.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Planes.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Planes.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "planes.html",
        title="Planes",
        active_tab="planes",
        rows=rows,
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/planes/add", methods=["POST"])
def planes_add():
    new_row = Planes(
        name=request.form.get("name"),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
        longitude=0,
        latitude=0,
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/planes")


# ============================================================
# SHIPS TAB
# ============================================================
@app.route("/ships")
def ships():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Ships.query

    if starts:
        query = query.filter(Ships.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Ships.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Ships.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "ships.html",
        title="Ships",
        active_tab="ships",
        rows=rows,
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/ships/add", methods=["POST"])
def ships_add():
    new_row = Ships(
        name=request.form.get("name"),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
        longitude=0,
        latitude=0,
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/ships")


# ============================================================
# TANKS TAB
# ============================================================
@app.route("/tanks")
def tanks():
    page = request.args.get("page", 1, type=int)

    # Read per_page from dropdown (default = 12)
    per_page = request.args.get("per_page", 10, type=int)

    starts = request.args.get("starts", "").strip()

    query = Tanks.query

    if starts:
        query = query.filter(Tanks.name.ilike(f"%{starts}%"))

    # If user selects "All" → per_page = 0
    if per_page == 0:
        rows = query.order_by(Tanks.name).all()
        total_pages = 1
        pagination = None
    else:
        pagination = db.paginate(
            query.order_by(Tanks.name), page=page, per_page=per_page
        )
        rows = pagination
        total_pages = pagination.pages

    return render_template(
        "tanks.html",
        title="Tanks",
        active_tab="tanks",
        rows=rows,
        starts=starts,
        per_page=per_page,
        total_pages=total_pages,
        pagination=pagination,
    )


@app.route("/tanks/add", methods=["POST"])
def tanks_add():
    new_row = Tanks(
        name=request.form.get("name"),
        comment=request.form.get("comment"),
        wiki=request.form.get("wiki"),
        longitude=0,
        latitude=0,
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect("/tanks")


# ============================================================
# UNIVERSAL DELETE ROUTE
# ============================================================
@app.route("/delete/<tab>/<int:id>")
def delete(tab, id):
    model_map = {
        "bcatp": Bcatp,
        "army": Army,
        "airforce": Airforce,
        "navy": Navy,
        "dewline": Dewline,
        "pinetree": Pinetree,
        "defunct": Defunct,
        "midcanada": Midcanada,
        "planes": Planes,
        "ships": Ships,
        "tanks": Tanks,
        "visitorcount": VisitorCount,
        "visitorlog": VisitorLog,
    }

    model = model_map.get(tab)
    if not model:
        return "Invalid tab", 400

    row = model.query.get(id)
    if not row:
        return "Record not found", 404

    db.session.delete(row)
    db.session.commit()
    return redirect(f"/{tab}")


@app.route("/global_search")
def global_search():
    q = request.args.get("query", "").strip().lower()
    if not q:
        return jsonify([])

    results = []
    per_page = 10  # MUST match your tab pagination

    tables = {
        "bcatp": Bcatp,
        "army": Army,
        "airforce": Airforce,
        "navy": Navy,
        "dewline": Dewline,
        "pinetree": Pinetree,
        "defunct": Defunct,
        "midcanada": Midcanada,
        "planes": Planes,
        "ships": Ships,
        "tanks": Tanks,
        "visitorcount": VisitorCount,
        "visitorlog": VisitorLog,
    }

    for tab, model in tables.items():

        # Get ALL rows sorted by name (not paginated)
        all_rows = model.query.order_by(model.name).all()

        # Loop through all rows and compute page number
        for index, r in enumerate(all_rows):

            # Match search
            if q in r.name.lower():

                # Compute correct page number
                page = (index // per_page) + 1

                # Add result with page included
                results.append({"tab": tab, "id": r.id, "name": r.name, "page": page})

    return jsonify(results)


# --------------------------------------------------------
# GLOBAL VISITOR COUNTER (SQL VERSION)
# ---------------------------------------------------------
from datetime import datetime, date  
from zoneinfo import ZoneInfo
@app.route("/visit", methods=["POST"])
def visit():
    data = request.get_json(silent=True) or {}
    is_owner = data.get("owner", False)

    vc = VisitorCount.query.first()

    previous_visit = vc.last_visit 
    now_local = datetime.now(ZoneInfo("America/Edmonton"))

    # Extract REAL visitor IP from Azure headers
    raw_ip = (
        request.headers.get("X-Client-IP")
        or request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Original-Forwarded-For")
        or request.remote_addr
    )

    # If multiple IPs or ports exist, clean it
    clean_ip = raw_ip.split(",")[0].split(":")[0]
    vc.last_ip = clean_ip

    vc.last_user_agent = request.headers.get("User-Agent")

    # Increment counters only for visitors
    if not is_owner:
        vc.count += 1

        if previous_visit is None or previous_visit.date() != date.today():
            vc.today_visits = 0

        vc.today_visits = (vc.today_visits or 0) + 1

    # NEW: Log every visit
    location = lookup_location(vc.last_ip)

    log = VisitorLog(
        ip=vc.last_ip,
        user_agent=vc.last_user_agent,
        is_owner=1 if is_owner else 0,
        location=location
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "ok"}), 200



@app.route("/getcount", methods=["GET"])
def getcount():
    vc = VisitorCount.query.first()
    return jsonify(
        {
            "count": vc.count,
            "today_visits": vc.today_visits,
            "last_visit": vc.last_visit,
            "last_ip": vc.last_ip,
            "last_user_agent": vc.last_user_agent,
        }
    )


@app.route("/visitlog", methods=["GET"])
def visitlog():
    logs = VisitorLog.query.order_by(VisitorLog.id.desc()).limit(100).all()
    return jsonify(
        [
            {
                "id": log.id,
                "timestamp": log.timestamp.isoformat(),
                "ip": log.ip,
                "user_agent": log.user_agent,
                "is_owner": log.is_owner,
                "location": log.location,   # <-- ADD THIS
            }
            for log in logs
        ]
    ) 

# ---------------------------------------------------------
# NOTIFY ROUTE (DISCORD WEBHOOK)
# ---------------------------------------------------------
import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

@app.route("/notify", methods=["POST"])
def notify():
    if not WEBHOOK_URL:
        return jsonify({"status": "error", "message": "Webhook not configured"}), 500
    
    try:
        requests.post(
            WEBHOOK_URL, json={"content": "Someone visited your JRD Projects page!"}
        )
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error"}), 500  

if __name__ == "__main__":
    app.run(debug=False)
