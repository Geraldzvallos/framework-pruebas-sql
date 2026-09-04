const API_URL = "http://127.0.0.1:8000/api";

function mostrarSeccion(seccion) {
    document.getElementById('seccion-casos').style.display = 'none';
    document.getElementById('seccion-suites').style.display = 'none';
    
    if (seccion === 'casos') {
        document.getElementById('seccion-casos').style.display = 'block';
        document.getElementById('titulo-seccion').innerText = "Gestión de Casos";
        cargarCasos();
    } else if (seccion === 'suites') {
        document.getElementById('seccion-suites').style.display = 'block';
        document.getElementById('titulo-seccion').innerText = "Gestión de Suites";
        cargarSuites();
    }
}

// GET: Cargar casos y actualizar KPI
async function cargarCasos() {
    try {
        const res = await fetch(`${API_URL}/test-cases/`);
        const casos = await res.json();
        
        // Actualizamos el KPI en tiempo real
        document.getElementById("kpi-total-casos").innerText = casos.length;
        
        const tbody = document.getElementById("tabla-casos");
        tbody.innerHTML = ""; 
        
        casos.forEach(c => {
            tbody.innerHTML += `
                <tr>
                    <td class="ps-4"><span class="badge bg-secondary">#${c.id}</span></td>
                    <td><strong class="text-dark">${c.name}</strong><br><small class="text-muted">${c.description}</small></td>
                    <td><code class="text-primary" style="font-size: 0.85rem; background: #f8f9fa; padding: 4px; border-radius: 4px;">${c.sql_query}</code></td>
                    <td><span class="badge bg-dark">${c.expected_result}</span></td>
                    <td class="pe-4 text-end">
                        <button class="btn btn-sm btn-outline-danger shadow-sm" onclick="eliminarCaso(${c.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (e) { 
        console.error("Error:", e); 
        Swal.fire('Error de Conexión', 'No se pudo conectar con FastAPI.', 'error');
    }
}

// POST: Crear nuevo caso desde el Modal
async function guardarNuevoCaso(event) {
    event.preventDefault(); // Evita que la página recargue
    
    const payload = {
        name: document.getElementById('tc-name').value,
        description: document.getElementById('tc-desc').value,
        sql_query: document.getElementById('tc-sql').value,
        expected_result: document.getElementById('tc-expected').value
    };

    try {
        const res = await fetch(`${API_URL}/test-cases/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            // Cerramos el modal usando Bootstrap JS
            const modalElement = document.getElementById('modalNuevoCaso');
            const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
            modal.hide();
            
            // Limpiamos el formulario
            document.getElementById('formNuevoCaso').reset();
            
            // Notificación Profesional
            Swal.fire({
                title: '¡Excelente!',
                text: 'El caso DML se ha registrado en la base de datos.',
                icon: 'success',
                timer: 2000,
                showConfirmButton: false
            });
            
            cargarCasos(); // Refresca la tabla y KPIs
        }
    } catch (e) {
        Swal.fire('Error', 'Fallo al guardar el registro.', 'error');
    }
}

// DELETE: Eliminar con SweetAlert2
function eliminarCaso(id) {
    Swal.fire({
        title: '¿Autoriza la eliminación?',
        text: `Se borrará permanentemente el caso de prueba #${id}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const res = await fetch(`${API_URL}/test-cases/${id}`, { method: 'DELETE' });
                if (res.ok) {
                    Swal.fire('Eliminado', `El caso #${id} fue purgado.`, 'success');
                    cargarCasos();
                } else {
                    Swal.fire('Error', 'El backend rechazó la petición.', 'error');
                }
            } catch (e) {
                Swal.fire('Error', 'Fallo de conexión.', 'error');
            }
        }
    });
}

// Mock para las suites
async function cargarSuites() {
    const contenedor = document.getElementById("contenedor-suites");
    contenedor.innerHTML = `
        <div class="col-md-6">
            <div class="card border-primary mb-3 shadow-sm">
                <div class="card-header bg-primary text-white"><i class="bi bi-box-seam me-2"></i> Suite ID: 1</div>
                <div class="card-body">
                    <h5 class="card-title text-dark">Suite MVP - Pruebas DML</h5>
                    <p class="card-text text-muted">Valida las operaciones de inserción, actualización y borrado en Oracle, verificando el Rollback automático.</p>
                </div>
                <div class="card-footer bg-transparent text-end">
                    <button class="btn btn-primary disabled"><i class="bi bi-play-fill"></i> Ejecutar Ráfaga (Oracle Pending)</button>
                </div>
            </div>
        </div>
    `;
}

// Inicializar la aplicación
mostrarSeccion('casos');