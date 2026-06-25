from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Producto
from app.cliente import cliente_bp
from app.extensions import db, bcrypt



@cliente_bp.route("/perfil")
@login_required
def perfil():
    return render_template("cliente/perfil.html", usuario=current_user)




@cliente_bp.route("/catalogo")
@login_required
def catalogo():
    if current_user.rol.lower() in ["admin", "administrador"]:
        return redirect(url_for("admin.dashboard"))

    productos = Producto.query.all()

    return render_template(
        "cliente/catalogo.html",
        usuario=current_user,
        productos=productos
    )


@cliente_bp.route("/mis_pedidos")
@login_required
def mis_pedidos():
    if current_user.rol.lower() in ["admin", "administrador"]:
        return redirect(url_for("admin.dashboard"))
    
    return render_template("cliente/mis_pedidos.html", usuario=current_user)


@cliente_bp.route("/perfil/actualizar", methods=["POST"])
@login_required
def actualizar_perfil():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")

    if nombre:
        current_user.nombre = nombre

    if telefono:
        current_user.telefono = telefono

    db.session.commit()
    flash("Perfil actualizado correctamente", "success")

    return redirect(url_for("cliente.perfil"))




@cliente_bp.route("/perfil/cambiar_password", methods=["POST"])
@login_required
def cambiar_password():

    password_actual = request.form.get("password_actual")
    nueva_password = request.form.get("password_nueva")
    confirmar = request.form.get("password_confirmar")

    if not bcrypt.check_password_hash(current_user.password, password_actual):
        flash("La contraseña actual es incorrecta.", "danger")
        return redirect(url_for("cliente.perfil"))

    if nueva_password != confirmar:
        flash("Las nuevas contraseñas no coinciden.", "danger")
        return redirect(url_for("cliente.perfil"))

    current_user.password = bcrypt.generate_password_hash(nueva_password).decode("utf-8")

    db.session.commit()

    flash("Contraseña actualizada correctamente.", "success")

    return redirect(url_for("cliente.perfil"))
