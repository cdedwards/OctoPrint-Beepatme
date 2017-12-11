/*
 * Author: ntoff
 * License: AGPLv3
 */
$(function() {
    function BeepatmeViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        
        //shoving this into the settings viewmodel because I'm too lazy to connect it otherwise
        self.settings.playAudio = function() {
            var audio = new Audio(self.settings.settings.plugins.beepatme.soundFile());
            audio.volume = self.settings.settings.plugins.beepatme.audioVolume() * 0.01;
            audio.play();
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "beepatme") {
                return;
            }
            self.settings.playAudio();
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: BeepatmeViewModel,
        dependencies: ["settingsViewModel"],
    });
});
