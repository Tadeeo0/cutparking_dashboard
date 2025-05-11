let map = null;
let markerLayer = null;

function showMap(lat, lng) {
  console.log('Mostrando el mapa con lat:', lat, 'y lng:', lng);

  const modalElement = document.getElementById('mapModal');
  const modal = $(modalElement); 

  function handleModalShown() {
    setTimeout(() => {
      console.log("Modal completamente visible, inicializando mapa");

      if (!map) {
        map = new ol.Map({
          target: 'map',
          layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM(),
            }),
          ],
          view: new ol.View({
            center: ol.proj.fromLonLat([lng, lat]),
            zoom: 18,
          }),
        });
      } else {
        map.getView().setCenter(ol.proj.fromLonLat([lng, lat]));
      }

      if (markerLayer) {
        map.removeLayer(markerLayer);
      }

      const marker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lng, lat])),
      });

      markerLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: [marker],
        }),
        style: new ol.style.Style({
          image: new ol.style.Icon({
            src: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
            scale: 0.05,
          }),
        }),
      });

      map.addLayer(markerLayer);
      map.updateSize();

      console.log("Mapa listo y actualizado");
    }, 300);

    $(modalElement).off('shown.bs.modal', handleModalShown);
  }

  $(modalElement).on('shown.bs.modal', handleModalShown);
  modal.modal('show');  
}
