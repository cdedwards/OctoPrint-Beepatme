/*
 * Author: ntoff
 * License: AGPLv3
 */
$(function() {
    function BeepatmeViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        
        //shoving this into the settings viewmodel because I'm too lazy to connect it otherwise
        self.settings.playAudio = function(sURL) {
            var audio = new Audio(sURL);
            audio.volume = self.settings.settings.plugins.beepatme.audioVolume() * 0.01;
            audio.play();
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "beepatme") {
                return;
            }
			
			if(data.cmd == "reload") {
				window.location.reload(true);
			} else {
				self.settings.playAudio(data.url);
			}
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: BeepatmeViewModel,
        dependencies: ["settingsViewModel"],
    });
});
