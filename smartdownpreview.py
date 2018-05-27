# Authors: Lan Guo, Dan Keith
# Plug-in for sublime text 3, opens up a user defined URL for preview Smartdown content
# To enable SmartDown rendering, opens up http://smartdown.site using the 'url=' feature, embed data in a data URI

import sublime
import sublime_plugin
import webbrowser
import base64
import os
import glob
import pdb
import time
import cgi
import re
from string import Template

useLocal = False

if useLocal:
	smartdownSite = 'https://127.0.0.1:4000'
else:
	smartdownSite = 'https://smartdown.site'

class SmartdownpreviewCommand(sublime_plugin.TextCommand):  #sublime_plugin.EventListener):

	# if outputMode is 'html', save out an html file; if outputMode is 'dataURI', open a browser for preview using smartdown.site
	outputMode = 'html' #'dataURI'

	#def on_post_save(self, view):
	def run(self, edit):
		# Template location is within the same package
		self.html_template_path = os.path.join(sublime.packages_path(), 'sublime-text-tools', 'smartdown_template.html')

		# saved file name, fullpath to the file being edited and saved
		self.currentFilePath = self.view.file_name()
		if self.currentFilePath.endswith('.md') or self.currentFilePath.endswith('.mmd'):
			currentFileName = os.path.basename(self.currentFilePath)
			content = open(self.currentFilePath, "r", encoding='utf-8').read()
			self.previewFilePath = os.path.join(os.path.expanduser("~"), 'tmp')
			if not os.path.exists(self.previewFilePath):
				os.mkdir(self.previewFilePath)
			previewFileFullPath = os.path.join(self.previewFilePath, "{}.html".format(currentFileName))

			currentFileDirectory = os.path.dirname(self.currentFilePath)

			def build_content_item(filepath):
				content = open(filepath, "r", encoding='utf-8').read()
				return {'id': os.path.basename(filepath), 'text': content}

			siblingContentItems = list(map(build_content_item, glob.glob(currentFileDirectory + '/*.md')))
			foundBase = False
			foundHome = False
			foundREADME = False
			for f in siblingContentItems:
				print('...content', f['id'], f['text'][:20])
				if f['id'] == 'Home.md':
					foundHome = True
				if f['id'] == currentFileName:
					foundBase = True
				if f['id'] == 'README.md':
					foundREADME = True

			if foundBase:
				base = currentFileName
			else:
				base = re.sub('\.md$', currentFileName, '')
				siblingContentItems = [build_content_item(self.currentFilePath)]

			def build_media_item(filepath):
				b64data = base64.b64encode(open(filepath, "rb").read())
				if filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
					mimetype = 'image/jpeg'
				if filepath.endswith('.png'):
					mimetype = 'image/png'
				if filepath.endswith('.js'):
					mimetype = 'application/javascript'
				if filepath.endswith('.gif'):
					mimetype = 'image/gif'
				dataURI = u'data:%s;base64,' % mimetype
				dataURI += b64data.decode('utf-8')
				return {'id': os.path.basename(filepath), 'text': dataURI}

			media_files = glob.glob(currentFileDirectory + '/*.png') +  \
							glob.glob(currentFileDirectory + '/*.js') +  \
							glob.glob(currentFileDirectory + '/*.gif') +  \
							glob.glob(currentFileDirectory + '/*.jpeg') +  \
							glob.glob(currentFileDirectory + '/*.jpg')
			siblingMediaItems = list(map(build_media_item, media_files))
			# for f in siblingMediaItems:
			# 	print('...media', f['id'], f['text'][:20])
			if not foundHome:
				siblingMediaItems = []

			print('foundHome', foundHome, ' foundREADME', foundREADME)
			hasREADMEAndHome = foundHome and foundREADME
			html_string = self.generate_html(
									title=currentFileName,
									base=base,
									contentItems=siblingContentItems,
									mediaItems=siblingMediaItems,
									smartdownSite=smartdownSite,
									hasREADMEAndHome=hasREADMEAndHome)
			self.save_tmp_file(html_string, outFilePath=previewFileFullPath)
			full_url = 'file://' + previewFileFullPath
			self.openUrl(full_url, currentFileName)

		else:
			self.log('This file is not SmartDown format!', self.currentFilePath)
			pass


	def generate_html(self, title, base, contentItems, mediaItems, smartdownSite, hasREADMEAndHome):
		'''
		Generates an html file from template and current file content, saves it locally.
		'''

		def escape_entities(contentItem):
			escapedText = cgi.escape(contentItem['text'])
			scriptText = '<script type="text/x-smartdown" id="' + contentItem['id'] + '">' + escapedText + '</script>'
			return scriptText
		escapedScripts = list(map(escape_entities, contentItems))


		# def escape_media(mediaItem):
		# 	mediaText = '<img style="width:100px;height:auto;border:1px solid red;" type="image/png" id="' + mediaItem['id'] + '" src="' + mediaItem['text'] + '"</img>'
		# 	return mediaText
		# escapedMedia = list(map(escape_media, mediaItems))

		def escape_media(mediaItem):
			mediaText = '{prefix: \'/block/' + mediaItem['id'] + '\', replace: \'' + mediaItem['text'] + '\'}'
			return mediaText
		escapedMedia = list(map(escape_media, mediaItems))
		mediaLinkRules = ',\n'.join(escapedMedia)
		html_template = open(self.html_template_path, "r").read()
		preview_html = Template(html_template).substitute(
							title=title,
							base=base,
							escapedScripts='\n\n\n\n'.join(escapedScripts),
							mediaLinkRules=mediaLinkRules,
							smartdownSite=smartdownSite,
							hasREADMEAndHome=hasREADMEAndHome)


		#pdb.set_trace()
		# Replace title and content in template with actual file we're editing
		# preview_html = html_template.replace('$title', title)
		# preview_html = preview_html.replace('$content', content)
		# preview_html = preview_html.replace('$smartdownSiteURL', smartdownSiteURL)
		# preview_html = preview_html.replace('$smartdownModulePrefix', smartdownModulePrefix)
		return preview_html

	def save_tmp_file(self, string, outFilePath):
		with open(outFilePath, 'w', encoding='utf-8') as outFile:
			outFile.write(string)

	def openUrl(self, url, currentFileName):
		url += '#' + currentFileName
		self.log('Opening '+url)
		webbrowser.open(url, new=0, autoraise=False)
		# https://docs.python.org/2/library/webbrowser.html
		# firefox = webbrowser.get('firefox')
		# firefox.open(url, new=0, autoraise=False)
		# time.sleep(1)
		# chrome_cmd = "open -a /Applications/Google\ Chrome.app \'%s\'" % url
		# print('###', chrome_cmd)
		# os.system(chrome_cmd)
		# time.sleep(1)
		# safari = webbrowser.get('safari')
		# safari.open(url, new=0, autoraise=False)
		# time.sleep(1)

	def log(self, msg):
		print(msg)
