# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class BeepatmePlugin(octoprint.plugin.SettingsPlugin,
					 octoprint.plugin.AssetPlugin,
					 octoprint.plugin.TemplatePlugin,
					 octoprint.plugin.EventHandlerPlugin):

	def __init__(self):
		self.done = False

	def get_settings_defaults(self):
		return dict(
			audioVolume=50,
			soundFile='/plugin/beepatme/static/audio/audio.mp3' #although this is a setting, changing it isn't implemented yet.
		)

	def on_event(self, event, payload):
		if "PrintDone" not in event:
			return event 
			return payload
		self._plugin_manager.send_plugin_message(self._identifier, dict(done=True)) 
		return event 
		return payload

	def get_assets(self):
		return dict(
			js=["js/beepatme.js"],
			css=["css/beepatme.css"],
			less=["less/beepatme.less"]
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False, name="Beep At Me")
		]

	def get_update_information(self):
		return dict(
			beepatme=dict(
				displayName="Beepatme Plugin",
				displayVersion=self._plugin_version,

				type="github_release",
				user="ntoff",
				repo="OctoPrint-Beepatme",
				current=self._plugin_version,

				pip="https://github.com/ntoff/OctoPrint-Beepatme/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Beepatme Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = BeepatmePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

