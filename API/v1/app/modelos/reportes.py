from bson.objectid import ObjectId
from app.index import mongo
from datetime import datetime

class ReportesModel:

    @staticmethod
    def ventas_por_usuario(id_usuario):
        try:
            ventas_cursor = mongo.db.ventas.find({"usuario_id": ObjectId(id_usuario)})
            ventas = []
            for venta in ventas_cursor:
                venta["_id"] = str(venta["_id"])
                venta["usuario_id"] = str(venta["usuario_id"])
                venta["prenda_id"] = str(venta["prenda_id"])
                if isinstance(venta.get("fecha"), datetime):
                    venta["fecha"] = venta["fecha"].isoformat()
                ventas.append(venta)
            return ventas
        except:
            return None

    @staticmethod
    def total_ventas_por_prenda():
        pipeline = [
            {
                "$group": {
                    "_id": "$prenda_id",
                    "total_vendido": {"$sum": "$cantidad"}
                }
            }
        ]
        resultados = list(mongo.db.ventas.aggregate(pipeline))
        # Convertir ObjectId a str y buscar nombre prenda
        reporte = []
        for r in resultados:
            prenda = mongo.db.prendas.find_one({"_id": ObjectId(r["_id"])})
            nombre_prenda = prenda["nombre"] if prenda else "Desconocida"
            reporte.append({
                "prenda_id": str(r["_id"]),
                "nombre_prenda": nombre_prenda,
                "total_vendido": r["total_vendido"]
            })
        return reporte

    @staticmethod
    def ventas_por_fecha(fecha_inicio, fecha_fin):
        try:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
            fecha_fin_dt = datetime.fromisoformat(fecha_fin)
        except:
            return None

        pipeline = [
            {
                "$match": {
                    "fecha": {
                        "$gte": fecha_inicio_dt,
                        "$lte": fecha_fin_dt
                    }
                }
            }
        ]
        ventas_cursor = mongo.db.ventas.aggregate(pipeline)
        ventas = []
        for venta in ventas_cursor:
            venta["_id"] = str(venta["_id"])
            venta["usuario_id"] = str(venta["usuario_id"])
            venta["prenda_id"] = str(venta["prenda_id"])
            if isinstance(venta.get("fecha"), datetime):
                venta["fecha"] = venta["fecha"].isoformat()
            ventas.append(venta)
        return ventas
