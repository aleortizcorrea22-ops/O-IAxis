# Deploy O-IAxis en la Nube

## PASO 1 - Supabase (base de datos PostgreSQL GRATIS)
1. Ir a https://supabase.com > crear cuenta con GitHub
2. New project: nombre 'oiaxis', region South America (Sao Paulo)
3. Settings > Database > Connection string > URI
4. Copiar: postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres

## PASO 2 - Railway (servidor Python GRATIS)
1. Ir a https://railway.app > crear cuenta con GitHub
2. New Project > Deploy from GitHub repo > seleccionar carpeta backend
3. Variables de entorno en Railway:
   DATABASE_URL = [URL de Supabase]
   SECRET_KEY   = [clave larga aleatoria]
   DEBUG        = False
   ENVIRONMENT  = production
   ALLOWED_ORIGINS = https://tu-frontend.vercel.app
4. URL resultante: https://oiaxis-api.up.railway.app

## PASO 3 - Vercel (frontend GRATIS)
1. Ir a https://vercel.com > New Project > carpeta frontend
2. Editar frontend/config.js antes de subir:
   window.OIAXIS_API_URL = 'https://oiaxis-api.up.railway.app';
3. URL resultante: https://oiaxis.vercel.app

## PASO 4 - Instalar en Android
1. Abrir Chrome en Android > ir a https://oiaxis.vercel.app
2. Menu 3 puntos > 'Agregar a pantalla de inicio'
3. Aparece como app con icono en el homescreen

## Costo: USD 0/mes (tiers gratuitos)
