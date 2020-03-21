$(document).ready(function(){
	let adel = $('.delete');
	for(let i=0; i<adel.length; i++){
		adel[i].onclick = function(){
			$.post('delete/' + this.id, function(){
				$(adel[i]).parent().parent().fadeOut('slow');
			});
		};
	}
});