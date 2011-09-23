/**
 * This class provides access to native mapping applications on the device.
 */
function Map() {
	
}

/**
 * Shows a native map on the device with pins at the given positions.
 * @param {Array} positions
 */
Map.prototype.show = function(positions) {

	var err = "map api is unimplemented on symbian.wrt";
	debug.log(err);
	return { name: "MapError", message: err };

};

if (typeof navigator.map == "undefined") navigator.map = new Map();
