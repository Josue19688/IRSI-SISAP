#!/bin/bash

# Forzar codificación UTF-8 en el entorno
export LANG=es_GT.UTF-8
export LC_ALL=es_GT.UTF-8

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

csv_dir="$SCRIPT_DIR/../data/compras"
template="$SCRIPT_DIR/../template/plantilla_facturas.tex"
output_dir="$SCRIPT_DIR/../data/facturas"
log="$SCRIPT_DIR/../data/log_diario.log"
pendientes="$SCRIPT_DIR/../data/pendientes_envio.csv"

mkdir -p "$output_dir"
: > "$pendientes"
: > "$log"

echo "Plantilla existe? $( [ -f "$template" ] && echo 'Sí' || echo 'No' )"

shopt -s nullglob
csv_files=("$csv_dir"/compras_*.csv)
shopt -u nullglob

echo "Archivos CSV encontrados: ${#csv_files[@]}"
for f in "${csv_files[@]}"; do echo " - $f"; done

if [ ${#csv_files[@]} -eq 0 ]; then
    echo "No se encontraron archivos CSV en $csv_dir"
    exit 1
fi

# Función para escapar caracteres LaTeX
escape_latex() {
    echo "$1" | sed \
        -e 's/\\/\\textbackslash{}/g' \
        -e 's/_/\\_/g' \
        -e 's/&/\\&/g' \
        -e 's/%/\\%/g' \
        -e 's/#/\\#/g' \
        -e 's/{/\\{/g' \
        -e 's/}/\\}/g' \
        -e 's/\$/\\\$/g' \
        -e 's/\^/\\^/g' \
        -e 's/~/\\~/g' \
        -e 's/"/''/g'
        # línea eliminada: -e "s/'/`/g"
}


for file in "${csv_files[@]}"; do
    echo "Procesando archivo: $file"

    tail -n +2 "$file" | while IFS=',' read -r id_transaccion fecha_emision nombre correo telefono direccion ciudad cantidad monto pago estado_pago ip timestamp observaciones; do
        echo "DEBUG: id_transaccion=$id_transaccion, nombre=$nombre, monto=$monto"

        # Escapar campos con caracteres especiales antes de usar en LaTeX
        nombre=$(escape_latex "$nombre")
        direccion=$(escape_latex "$direccion")
        ciudad=$(escape_latex "$ciudad")
        observaciones=$(escape_latex "$observaciones")
        correo=$(escape_latex "$correo")
        telefono=$(escape_latex "$telefono")
        pago=$(escape_latex "$pago")
        estado_pago=$(escape_latex "$estado_pago")

        nombre_archivo="factura_${id_transaccion}.tex"
        tex="$output_dir/$nombre_archivo"
        pdf="${tex/.tex/.pdf}"

        sed -e "s|{id_transaccion}|$id_transaccion|g" \
            -e "s|{fecha_emision}|$fecha_emision|g" \
            -e "s|{nombre}|$nombre|g" \
            -e "s|{correo}|$correo|g" \
            -e "s|{telefono}|$telefono|g" \
            -e "s|{direccion}|$direccion|g" \
            -e "s|{ciudad}|$ciudad|g" \
            -e "s|{cantidad}|$cantidad|g" \
            -e "s|{monto}|$monto|g" \
            -e "s|{pago}|$pago|g" \
            -e "s|{estado_pago}|$estado_pago|g" \
            -e "s|{ip}|$ip|g" \
            -e "s|{timestamp}|$timestamp|g" \
            -e "s|{observaciones}|$observaciones|g" \
            "$template" > "$tex"

        echo "DEBUG: Archivo .tex generado: $tex"
        ls -l "$tex"
        head -5 "$tex"

        pdflatex -interaction=nonstopmode -output-directory="$output_dir" "$tex" 2>&1 | tee -a "$log"

        if [ $? -eq 0 ]; then
            echo "✅ Factura generada: $pdf"
            echo "$pdf,$correo" >> "$pendientes"
        else
            echo "❌ Error al generar PDF para ID: $id_transaccion" >> "$log"
        fi

        # rm "$tex"  # Comentar para depurar
    done
done

echo "✅ Script completado."
