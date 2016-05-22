$(document).ready(function() {
	$("#realtime").hide();
	$("#time").mouseenter(function() {
		$("#relatime").fadeOut("fast", function() {
			$("#realtime").fadeIn("fast");
		});
	}).mouseleave(function() {
		$("#realtime").fadeOut("fast", function() {
			$("#relatime").fadeIn("fast");
		});
	});
});
