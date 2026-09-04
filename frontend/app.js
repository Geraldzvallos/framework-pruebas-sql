const API_URL = "http://127.0.0.1:8000/api";

function mostrarSeccion(seccion) {
    // 1. Ocultar las pantallas
    document.getElementById('seccion-casos').style.display = 'none';
    document.getElementById('seccion-suites').style.display = 'none';
    
    // 2. Limpiar el color azul de todo el menú
    const links = document.querySelectorAll('.sidebar a');
    links.forEach(link => link.classList.remove('active'));
    
    // 3. Mostrar la pantalla correcta y pintar su botón
    if (seccion === 'casos') {
        document.getElementById('seccion-casos').style.display = 'block';
        document.getElementById('titulo-seccion').innerText = "Gestión de Casos";
        links[0].classList.add('active'); // Pinta Casos
        cargarCasos();
    } else if (seccion === 'suites') {
        document.getElementById('seccion-suites').style.display = 'block';
        document.getElementById('titulo-seccion').innerText = "Gestión de Suites";
        links[1].classList.add('active'); // Pinta Suites
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

// --- SUITES DE PRUEBAS (DINÁMICO) ---
async function cargarSuites() {
    try {
        const res = await fetch(`${API_URL}/suites/`);
        const suites = await res.json();
        
        // Actualizamos el KPI de Suites
        document.getElementById("kpi-total-suites").innerText = suites.length;
        
        const contenedor = document.getElementById("contenedor-suites");
        contenedor.innerHTML = ""; 
        
        if (suites.length === 0) {
            contenedor.innerHTML = `<div class="col-12 text-center text-muted mt-4">No hay suites registradas.</div>`;
            return;
        }

        suites.forEach(s => {
            // Contamos cuántos casos tiene asociados esta suite
            const numCasos = s.test_cases ? s.test_cases.length : 0;
            
            contenedor.innerHTML += `
                <div class="col-md-6 mb-4">
                    <div class="card border-primary shadow-sm h-100">
                        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                            <span><i class="bi bi-box-seam me-2"></i> Suite ID: #${s.id}</span>
                            <span class="badge bg-light text-primary">${numCasos} Casos</span>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title text-dark fw-bold">${s.name}</h5>
                            <p class="card-text text-muted">${s.description}</p>
                        </div>
                        <div class="card-footer bg-transparent border-top-0 text-end">
                            <button class="btn btn-primary" onclick="lanzarSuite(${s.id})">
                                <i class="bi bi-play-fill me-1"></i> Ejecutar Ráfaga
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error("Error al cargar suites:", e);
        Swal.fire('Error', 'No se pudieron cargar las Suites de Ejecución.', 'error');
    }
}

// Función preparada para cuando conectemos Oracle
function lanzarSuite(id) {
    Swal.fire({
        title: 'Motor en Espera',
        text: `La suite #${id} está lista, pero la conexión a Oracle objetivo aún no ha sido configurada.`,
        icon: 'info',
        confirmButtonText: 'Entendido'
    });
}

// Inicializar la aplicación
mostrarSeccion('casos');