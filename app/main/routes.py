from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.main import main_bp

from app.models import Producto
from app.extensions import db, bcrypt


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.rol.lower() in ["admin", "administrador"]:
            return redirect(url_for("admin.dashboard")) 
        else:
            return redirect(url_for("main.pedidos"))
    return render_template("main/index.html")

@main_bp.route("/administracion")
@login_required
def administracion():
    if current_user.rol.lower() not in ["admin", "administrador"]:
        flash("Acceso denegado. Solo administradores pueden acceder a esta sección.", "error")
        return redirect(url_for("main.pedidos"))
    return redirect(url_for("admin.dashboard"))

@main_bp.route("/pedidos")
@login_required
def pedidos():

    return redirect(url_for("main.catalogo"))
    return render_template("main/pedidos.html", usuario=current_user)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.rol.lower() in ["admin", "administrador"]:
        return redirect(url_for("admin.dashboard"))  
    else:
        return redirect(url_for("main.pedidos"))

@main_bp.route("/perfil")
@login_required
def perfil():
    return render_template("main/perfil.html", usuario=current_user)

@main_bp.route("/check-auth")
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "usuario": {
                "id": current_user.id_usuario,
                "nombre": current_user.nombre,
                "email": current_user.email,
                "rol": current_user.rol
            }
        })
    else:
        return jsonify({"authenticated": False})

@main_bp.route("/check-role")
@login_required
def check_role():
    if current_user.rol.lower() in ["admin", "administrador"]:
        rol = "administrador"
    else:
        rol = "cliente"
    
    return jsonify({
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol,
        "tipo": rol,
        "es_administrador": current_user.rol.lower() in ["admin", "administrador"]
    })




@main_bp.route("/catalogo")
@login_required
def catalogo():
    if current_user.rol.lower() in ["admin", "administrador"]:
        return redirect(url_for("admin.dashboard"))

    productos = Producto.query.all()

    return render_template(
        "main/catalogo.html",
        usuario=current_user,
        productos=productos
    )


@main_bp.route("/mis_pedidos")
@login_required
def mis_pedidos():
    if current_user.rol.lower() in ["admin", "administrador"]:
        return redirect(url_for("admin.dashboard"))
    
    return render_template("main/mis_pedidos.html", usuario=current_user)


@main_bp.route("/perfil/actualizar", methods=["POST"])
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

    return redirect(url_for("main.perfil"))




@main_bp.route("/perfil/cambiar_password", methods=["POST"])
@login_required
def cambiar_password():

    password_actual = request.form.get("password_actual")
    nueva_password = request.form.get("password_nueva")
    confirmar = request.form.get("password_confirmar")

    if not bcrypt.check_password_hash(current_user.password, password_actual):
        flash("La contraseña actual es incorrecta.", "danger")
        return redirect(url_for("main.perfil"))

    if nueva_password != confirmar:
        flash("Las nuevas contraseñas no coinciden.", "danger")
        return redirect(url_for("main.perfil"))

    current_user.password = bcrypt.generate_password_hash(nueva_password).decode("utf-8")

    db.session.commit()

    flash("Contraseña actualizada correctamente.", "success")

    return redirect(url_for("main.perfil"))












