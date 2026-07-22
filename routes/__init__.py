from flask import Flask
from .student_routes import student_bp
from .admin_routes import admin_bp
from .room_routes import room_bp
from .allocation_routes import allocation_bp  # <-- Import karo

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(student_bp)          # / (index), /book, /status, /api/occupancy, /rooms
    app.register_blueprint(admin_bp, url_prefix='/admin')  # /admin/login, /admin/dashboard, etc.
    app.register_blueprint(room_bp, url_prefix='/rooms')   # Optional
    app.register_blueprint(allocation_bp)       # /allocations, /allocations/api