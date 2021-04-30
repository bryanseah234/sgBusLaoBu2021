document.addEventListener('DOMContentLoaded', () => {
    pageLoad();
});

function onlyAllowOneCall(fn){
     var hasBeenCalled = false;    
     return function(){
          if (hasBeenCalled){
               throw Error("Attempted to call callback twice")
          }
          hasBeenCalled = true;
          return fn.apply(this, arguments)
     }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(showPosition);
    }       
}

function showPosition(position, callback) {
    callback = onlyAllowOneCall(callback)


    console.log(position);
    document.frm1.getlat.value = position.coords.latitude;
    document.frm1.getlon.value = position.coords.longitude;
    slider = document.getElementById('slider');
    // slider.oninput = function() {
    //     document.frm1.getslider.value = this.value;
    // }
    document.frm1.getslider.value = slider.value;
    document.frm1.submit();


    longitude = document.getElementById('getlon').value;
    latitude = document.getElementById('getlat').value;
    slider = document.getElementById('getslider').value;

    // var coordinates = lon+','+lat;
    // console.log(coordinates)
    const URL = '/findabus'
    const xhr = new XMLHttpRequest();
    sender = JSON.stringify(coordinates)
    xhr.open('POST', URL);
    xhr.send(sender);
}

function positionError(error) {
    if (error.PERMISSION_DENIED) alert('please let Laobu get your location');
    hideLoadingDiv();
    showError('Laobu could not determine your location :(, Laobu needs you to refresh the page and click "allow"');
}

function pageLoad() {
    getLocation();
}
