# Vibe Report — EcoTrack

## Configuración de las reglas del agente

Para iniciar EcoTrack configuré un archivo `.cursorrules` en la raíz del proyecto. Allí definí el contexto del MVP, el uso de Python y Streamlit, y reglas orientadas a mantener un código limpio, modular y fácil de desplegar.

También establecí que el agente debía evitar la sobreingeniería, separar la interfaz de la lógica de procesamiento, conservar la funcionalidad existente durante las iteraciones, manejar entradas inválidas y verificar la aplicación después de cambios importantes.

Mi intención fue darle al agente un marco de trabajo claro antes de solicitar código. En lugar de repetir las mismas restricciones en cada prompt, las reglas funcionaron como un contexto persistente para mantener las decisiones técnicas alineadas con la visión del producto.

## Dificultades al delegar el código a la IA

La principal dificultad fue comprobar que una solución generada y aparentemente funcional no necesariamente cubre todos los comportamientos esperados.

La primera versión procesaba correctamente el ejemplo principal, pero al probar otras expresiones encontré problemas. Por ejemplo, la frase:

> “Hoy comí pollo, viajé 10 km en carro y 5 km en bus”

no reconocía inicialmente el trayecto en carro.

También encontré una limitación con:

> “Hoy manejé 15 km y comí pescado”

porque el transporte no era interpretado.

En lugar de modificar manualmente el código, describí al agente las entradas utilizadas, el resultado obtenido y el comportamiento esperado. Claude Code analizó la causa raíz, corrigió la lógica y añadió pruebas automatizadas para comprobar tanto los casos nuevos como los anteriores.

Durante el despliegue también aparecieron dificultades relacionadas con Replit, como límites diarios del agente y la necesidad de configurar correctamente el comando de ejecución para producción. Esto mostró que la orquestación no consiste solamente en generar código, sino también en gestionar las restricciones de las herramientas utilizadas.

## De escribir código a orquestar una visión

El cambio más evidente fue pasar de pensar primero en cómo implementar cada función a concentrarme en qué debía hacer la aplicación y cómo debía sentirse.

Mi rol consistió principalmente en definir objetivos, establecer restricciones, evaluar propuestas de arquitectura, probar comportamientos, detectar problemas y refinar instrucciones.

En la iteración visual, por ejemplo, definí un “vibe” moderno, minimalista y relacionado con sostenibilidad, mientras el agente tradujo esa intención a componentes de Streamlit, estilos y decisiones de interfaz.

La experiencia me permitió entender que Vibe Coding no elimina la responsabilidad técnica del desarrollador. Al contrario, cambia su función. La IA puede ejecutar gran parte de la implementación, pero el humano sigue siendo responsable de evaluar, decidir y validar.

El código dejó de ser el centro del proceso y pasó a ser el resultado de una dinámica de orquestación donde mi responsabilidad principal fue mantener la visión y la calidad del producto.