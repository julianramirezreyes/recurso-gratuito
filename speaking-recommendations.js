(function (root, factory) {
  const api = factory();

  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  } else {
    root.SpeakingRecommendations = api;
    if (root.document?.getElementById('showRecommendations')) {
      api.init(root.document);
    }
  }
})(typeof window === 'undefined' ? globalThis : window, function () {
  const recommendations = [
    {
      title: 'Me quedo en blanco.',
      exercise: 'Elige una idea sencilla y anota tres palabras clave, no frases completas. Habla durante 30 segundos; si te detienes, mira la siguiente palabra y retoma desde ahí.',
      marker: '¿Pudiste recuperar el hilo usando una palabra clave, sin leer un guion?',
      source: 'Concordia University · Presentation notes',
      url: 'https://www.concordia.ca/students/success/learning-support/resources/oral-presentations/presentation-notes.html',
    },
    {
      title: 'Repito mucho las mismas palabras.',
      exercise: 'Graba 30 segundos contando algo cotidiano. Escucha y anota una palabra que se repite; decide si alguna repetición te distrae y, si quieres, reformula solo una para comparar ambas versiones.',
      marker: '¿La repetición cumple una función —por ejemplo, enfatizar— o distrae de la idea?',
      caveat: 'Es una adaptación de autoobservación, no una regla para evitar repetir palabras: a veces la repetición sirve para enfatizar una idea.',
      source: 'MIT Biological Engineering Communication Lab · Public Speaking: How to Practice Effectively',
      url: 'https://mitcommlab.mit.edu/be/commkit/public-speaking-how-to-practice/',
    },
    {
      title: 'Hablo demasiado rápido.',
      exercise: 'Explica una idea en 30–45 segundos. Marca con una barra dónde termina cada idea y vuelve a decirla haciendo una pausa breve en cada barra.',
      marker: '¿Puedes identificar cada idea al escuchar la segunda toma?',
      source: 'Stanford Oral Communication Program · Delivery',
      url: 'https://oralcommprogram.stanford.edu/presentation-and-delivery/delivery',
    },
    {
      title: 'Termino las frases sin fuerza.',
      exercise: 'Lee cuatro frases breves y marca el final de cada una. Graba una toma a volumen y tono cómodos, dejando que la última palabra se complete sin empujar la voz.',
      marker: '¿Se escucha completa la última palabra de cada frase?',
      caveat: 'Esto es una práctica de observación, no una evaluación de la voz. Si el cambio de voz persiste o causa molestias, consulta a un profesional de la voz.',
      source: 'American Speech-Language-Hearing Association · Voice Disorders',
      url: 'https://www.asha.org/practice-portal/clinical-topics/voice-disorders/',
    },
    {
      title: 'Uso muchas muletillas.',
      exercise: 'Explica un tema durante 30 segundos y cuenta una sola muletilla que notes. Repite la explicación; en algunos momentos, cambia esa muletilla por una pausa breve. No hace falta eliminar todas.',
      marker: '¿En qué momento una pausa te ayudó a continuar con más claridad?',
      source: 'Stanford Oral Communication Program · Delivery',
      url: 'https://oralcommprogram.stanford.edu/presentation-and-delivery/delivery',
    },
    {
      title: 'No encuentro la palabra exacta.',
      exercise: 'Elige cinco objetos o ideas. Si una palabra no aparece, descríbela con su categoría, función o una característica y luego intenta recuperar su nombre.',
      marker: '¿Lograste transmitir la idea mientras buscabas la palabra?',
      caveat: 'El artículo enlazado es un estudio observacional de 43 personas con afasia postictus que analiza la relación entre circunloquios y medidas del discurso; no evalúa una intervención ni establece eficacia clínica. Esta actividad es solo una adaptación práctica, no terapia.',
      source: 'PMC · Evaluating circumlocution in naming as a predictor of communicative informativeness and efficiency in discourse',
      url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10977788/',
    },
    {
      title: 'Me cuesta explicar mis ideas.',
      exercise: 'Escoge una idea y anota tres puntos: idea principal, una razón y un ejemplo. Explícala en voz alta durante 30–45 segundos siguiendo ese orden.',
      marker: '¿Puede otra persona reconocer la idea, la razón y el ejemplo?',
      source: 'University of Sydney · Structure a presentation',
      url: 'https://www.sydney.edu.au/students/study-skills/oral-presentations/structure-presentation.html',
    },
    {
      title: 'Mi voz tiembla o pierde volumen.',
      exercise: 'Lee un párrafo corto con tu voz habitual y a un volumen cómodo. Graba una toma y escucha si las palabras finales siguen siendo audibles; no aumentes el volumen ni fuerces la voz.',
      marker: '¿Puedes oír las últimas palabras manteniendo una sensación cómoda al hablar?',
      caveat: 'No fuerces la voz. Si la dificultad persiste o hay molestias, un profesional de la voz puede orientarte.',
      source: 'American Speech-Language-Hearing Association · Voice Disorders',
      url: 'https://www.asha.org/practice-portal/clinical-topics/voice-disorders/',
    },
    {
      title: 'Me cuesta hablar frente a otras personas.',
      exercise: 'Elige un paso de baja presión: enviar a alguien de confianza una nota de voz de 30–45 segundos sobre un tema conocido. Repite el mismo paso una vez si te resulta manejable.',
      marker: '¿Completaste el paso elegido y qué nivel de comodidad notaste antes y después?',
      caveat: 'Avanza de forma gradual y sin forzarte. Si la evitación afecta tu vida cotidiana, considera hablar con un profesional de salud mental.',
      source: 'National Institute of Mental Health · Social Anxiety Disorder',
      url: 'https://www.nimh.nih.gov/health/publications/social-anxiety-disorder-more-than-just-shyness',
    },
  ];

  function renderCard(recommendation, index) {
    const caveat = recommendation.caveat
      ? `<p class="recommendation-caveat"><strong>Ten en cuenta:</strong> ${recommendation.caveat}</p>`
      : '';

    return `
      <article class="recommendation-card">
        <p class="recommendation-label">Señal ${index + 1}</p>
        <h3>${recommendation.title}</h3>
        <p class="recommendation-duration"><strong>Práctica de 3–5 minutos:</strong> ${recommendation.exercise}</p>
        <p><strong>Observa:</strong> ${recommendation.marker}</p>
        ${caveat}
        <a class="recommendation-source" href="${recommendation.url}" target="_blank" rel="noopener noreferrer">Fuente: ${recommendation.source}</a>
      </article>`;
  }

  function init(document) {
    const checkboxes = [...document.querySelectorAll('#diagnostico .diagnostic-signals input[type="checkbox"]')];
    const button = document.getElementById('showRecommendations');
    const results = document.getElementById('recommendationResults');
    const heading = document.getElementById('recommendationHeading');
    const cards = document.getElementById('recommendationCards');
    const status = document.getElementById('recommendationStatus');
    let hasRequestedResults = false;

    button.addEventListener('click', () => {
      hasRequestedResults = true;
      const selected = checkboxes.flatMap((checkbox, index) => checkbox.checked ? [{ recommendation: recommendations[index], index }] : []);

      if (selected.length === 0) {
        cards.innerHTML = '';
        results.hidden = true;
        status.textContent = 'Marca al menos una señal para ver tus recomendaciones.';
        return;
      }

      cards.innerHTML = selected.map(({ recommendation, index }) => renderCard(recommendation, index)).join('');
      results.hidden = false;
      status.textContent = `Se muestran ${selected.length} ${selected.length === 1 ? 'recomendación' : 'recomendaciones'} personalizadas.`;
      heading.focus();
    });

    checkboxes.forEach((checkbox) => checkbox.addEventListener('change', () => {
      if (!hasRequestedResults) return;

      cards.innerHTML = '';
      results.hidden = true;
      status.textContent = 'Cambiaste la selección. Vuelve a pulsar «Ver mis recomendaciones» para actualizar los resultados.';
      hasRequestedResults = false;
    }));
  }

  return { init };
});
