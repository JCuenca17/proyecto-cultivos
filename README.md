🌱 AgroPredic: Sistema de Predicción de Demanda Sostenible

Optimización agrícola inteligente: Predicción de demanda basada en datos históricos y ajuste climático en tiempo real para reducir el desperdicio de cultivos (Palta, Mango, Arándanos).

📖 Descripción del Proyecto

AgroPredic es una solución SaaS diseñada para ayudar a los agricultores a tomar decisiones de siembra informadas. El sistema utiliza un algoritmo de promedios ponderados ajustados por tendencias y factores de riesgo climático (como El Niño o La Niña) para calcular el volumen de producción óptimo.

Este proyecto ha sido desarrollado bajo estrictos estándares de Ingeniería de Software:

ISO/IEC 25000 (SQuaRE): Para la gestión de requisitos de calidad, usabilidad y adecuación funcional.

ISO/IEC 5055: Para asegurar la integridad estructural, seguridad, fiabilidad y mantenibilidad del código fuente.

🚀 Características Principales

1. Gestión de Datos

📝 Ingreso Manual: Formulario intuitivo para registrar ventas diarias.

📂 Carga Masiva: Importación de grandes volúmenes de datos históricos vía CSV.

2. Motor de Inteligencia (Predictor)

📊 Algoritmo Ponderado: Da más peso a los datos recientes para detectar tendencias de mercado (+/- 5%).

⛈️ Ajuste Climático: Reduce automáticamente la sugerencia de siembra si se detectan riesgos (Ej: "El Niño" reduce un 20%).

3. Monitor Climático

Registro de temperatura, precipitación y eventos fenomenológicos.

Sistema de alertas visuales (🟢 Seguro / 🟡 Precaución / 🔴 Peligro).

4. Calidad y Reportes

Reportes de ventas detallados listos para imprimir.

Dashboard con KPIs financieros y operativos.

🛠️ Tecnologías y Herramientas

Backend: Python (Flask)

Base de Datos: SQLite

Frontend: HTML5, CSS3 (Diseño Enterprise/SaaS), FontAwesome

Análisis de Datos: Pandas

Calidad & Testing:

unittest (Pruebas Unitarias / ISO 5055 Dinámica)

SonarQube (Análisis Estático / ISO 5055 Estática)

Jira (Gestión del Proceso / ISO 25000)

⚙️ Instalación y Uso

Sigue estos pasos para ejecutar el proyecto en tu computadora:

Prerrequisitos

Tener instalado Python y Git.

1. Clonar el repositorio

git clone [https://github.com/TU_USUARIO/AgroPredic.git](https://github.com/TU_USUARIO/AgroPredic.git)
cd AgroPredic


2. Crear entorno virtual

python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate


3. Instalar dependencias

pip install Flask pandas


4. Inicializar la Base de Datos

python setup_db.py


(Verás un mensaje confirmando que cultivos.db ha sido creada)

5. Ejecutar la Aplicación

python app.py


Abre tu navegador y ve a: http://127.0.0.1:5000

🧪 Ejecución de Pruebas de Calidad (ISO 5055)

Para validar la robustez del sistema y verificar que la lógica climática (El Niño/La Niña) funciona correctamente, ejecuta el script de pruebas automatizadas:

python tests.py


Resultado esperado:

--- EJECUTANDO CERTIFICACIÓN DE CALIDAD COMPLETA ---
✅ Test 1: Web disponible... OK
✅ Test 2: Guardado de datos... OK
✅ Test 3: Lógica de Mercado... OK
✅ Test 4: Escenario El Niño (-20%)... OK
...
Ran 7 tests in 0.05s
OK


Curso: Calidad de Software

Universidad Nacional de San Agustín

Año: 2025
