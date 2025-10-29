/**
 * Mapea el nombre de un país a su código de moneda ISO 4217.
 * Se usa para llenar dinámicamente la columna 'Moneda'.
 */
function obtenerCodigoMoneda(pais) {
    // Usamos toLocaleLowerCase() para manejar mayúsculas/minúsculas inconsistentes
    const paisLower = pais.trim().toLowerCase(); 

    if (paisLower.includes('chile')) {
        return 'CLP';
    } else if (paisLower.includes('colombia')) {
        return 'COP';
    } else if (paisLower.includes('perú') || paisLower.includes('peru')) {
        return 'PEN';
    }
}

/**
 * Recorre la tabla y rellena la columna 'Moneda' basándose en la columna 'País'.
 */
function actualizarCodigosMonedaEnTabla() {
    const tabla = document.querySelector('.tabla-calificaciones');
    
    // Si la tabla no existe o está vacía, salimos
    if (!tabla || tabla.querySelector('.sin-registros')) {
        return;
    }

    const filas = tabla.querySelectorAll('tbody tr');
    let indicePais = -1;
    let indiceMoneda = -1;

    // 1. Encontrar los índices de las columnas "País" y "Moneda"
    const encabezados = tabla.querySelectorAll('thead th');
    encabezados.forEach((th, index) => {
        const texto = th.textContent.trim().toLowerCase();
        if (texto.includes('país')) {
            indicePais = index;
        } else if (texto.includes('moneda')) {
            indiceMoneda = index;
        }
    });

    // Verificar que ambas columnas existen
    if (indicePais === -1 || indiceMoneda === -1) {
        console.error("Error: No se encontró la columna 'País' o 'Moneda' en los encabezados de la tabla.");
        return;
    }

    // 2. Iterar sobre las filas y actualizar
    filas.forEach(fila => {
        const celdas = fila.querySelectorAll('td');
        
        // La celda del país contiene el nombre (ej: "Chile")
        const celdaPais = celdas[indicePais];
        
        // La celda de la moneda es la que vamos a escribir (ej: "CLP")
        const celdaMoneda = celdas[indiceMoneda];

        if (celdaPais && celdaMoneda) {
            const nombrePais = celdaPais.textContent.trim();
            const codigoMoneda = obtenerCodigoMoneda(nombrePais);
            
            // Escribir el código en la columna 'Moneda'
            celdaMoneda.innerHTML = `<span class="codigo-moneda">${codigoMoneda}</span>`;
        }
    });
}

// Ejecutar la función cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', actualizarCodigosMonedaEnTabla);