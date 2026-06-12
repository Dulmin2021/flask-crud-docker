from flask import Blueprint, jsonify, request
from . import db
from .models import Item

items_bp = Blueprint("items", __name__, url_prefix="/items")


# ── Health check ────────────────────────────────────────────────────────────
@items_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ── GET all items ────────────────────────────────────────────────────────────
@items_bp.route("/", methods=["GET"])
def get_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items]), 200


# ── GET single item ──────────────────────────────────────────────────────────
@items_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id, description="Item not found")
    return jsonify(item.to_dict()), 200


# ── POST create item ─────────────────────────────────────────────────────────
@items_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    item = Item(
        name=data["name"],
        description=data.get("description"),
        quantity=data.get("quantity", 0),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


# ── PUT update item ──────────────────────────────────────────────────────────
@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id, description="Item not found")
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    item.name        = data.get("name",        item.name)
    item.description = data.get("description", item.description)
    item.quantity    = data.get("quantity",    item.quantity)
    db.session.commit()
    return jsonify(item.to_dict()), 200


# ── DELETE item ──────────────────────────────────────────────────────────────
@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id, description="Item not found")
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Item {item_id} deleted"}), 200
