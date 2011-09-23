/**
 * This class provides access to the device SMS functionality.
 * @constructor
 */
function Sms() {

}

/**
 * Sends an SMS message.
 * @param {Integer} number The phone number to send the message to.
 * @param {String} message The contents of the SMS message to send.
 * @param {Function} successCallback The function to call when the SMS message is sent.
 * @param {Function} errorCallback The function to call when there is an error sending the SMS message.
 * @param {PositionOptions} options The options for accessing the GPS location such as timeout and accuracy.
 */
Sms.prototype.send = function(number, message, successCallback, errorCallback, options) {
    try {
		if (!this.serviceObj)
			this.serviceObj = this.getServiceObj();
			
	    // Setup input params using dot syntax
	    var criteria = new Object();
	    criteria.MessageType = 'SMS';
	    criteria.To = number;
	    criteria.BodyText = message;

      	var result = this.serviceObj.IMessaging.Send(criteria);
    	if (result.ErrorCode != 0 && result.ErrorCode != "0")
		{
			var exception = { name: "SMSError", message: result.ErrorMessage };
			throw exception;
		} else {
			successCallback.call();
		}
    }
  	catch(ex)
  	{
		errorCallback.call({ name: "SmsError", message: ex.name + ": " + ex.message });
  	}

};


//gets the Sms Service Object from WRT
Sms.prototype.getServiceObj = function() {
	var so;
	
    try {
        so = device.getServiceObject("Service.Messaging", "IMessaging");
    } catch (ex) {
		throw {
			name: "SmsError",
			message: "Failed to load sms service (" + ex.name + ": " + ex.message + ")"
		};
    }		
	return so;
};

if (typeof navigator.sms == "undefined") navigator.sms = new Sms();