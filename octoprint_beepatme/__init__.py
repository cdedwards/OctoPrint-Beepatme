# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import octoprint.filemanager
import octoprint.filemanager.util

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

	def on_event(self, event, payload): #oh yeah, note to self: mess about with this malarky. print cancel, print done, maybe print started? I dunno how far I wanna go
		if "PrintDone" not in event:	#either way, fix it
			return (event, payload)
		self._plugin_manager.send_plugin_message(self._identifier, dict(url=self._settings.get(["soundFile"]))) 
		return (event, payload)

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
		
	def get_extension_tree(self, *args, **kwargs):
		return dict(
			machinecode=dict(
				custombackground=["mp3","wav","ogg"]
			)
		)
	
	def custombeepupload(self, path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
		file_extensions = [".mp3", ".wav", ".ogg"]
		name, extension = os.path.splitext(file_object.filename)
		if extension in file_extensions:
			octoprint.filemanager.util.StreamWrapper(self.get_plugin_data_folder() + "/uploaded" + extension, file_object.stream()).save(self.get_plugin_data_folder() + "/uploaded" + extension)
			self._settings.set(["soundFile"],"/plugin/beepatme/uploaded" + extension)
			self._settings.save()
			self._plugin_manager.send_plugin_message(self._identifier, dict(cmd="reload"))
		return file_object

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
		
	def route_hook(self, server_routes, *args, **kwargs):
		from octoprint.server.util.tornado import LargeResponseHandler, UrlProxyHandler, path_validation_factory
		from octoprint.util import is_hidden_path

		return [
				(r"/(.*)", LargeResponseHandler, dict(path=self.get_plugin_data_folder(),
																as_attachment=True,
																path_validation=path_validation_factory(lambda path: not is_hidden_path(path),status_code=404)))
				]

__plugin_name__ = "Beepatme Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = BeepatmePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.filemanager.extension_tree": __plugin_implementation__.get_extension_tree,
		"octoprint.filemanager.preprocessor": __plugin_implementation__.custombeepupload,
		"octoprint.server.http.routes": __plugin_implementation__.route_hook
	}

