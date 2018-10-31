# -*- coding: utf-8 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class ExtractCentroid:
	def __init__(self, iface):
		self.iface = iface
		self.canvas = iface.mapCanvas()

	def initGui(self):
		self.action = QAction(QIcon(":/plugins/"), "&ExtractCentroid", self.iface.mainWindow())
		QObject.connect(self.action, SIGNAL("activated()"), self.extract_centroid)
		self.iface.addPluginToMenu("ExtractCentroid", self.action)

	def unload(self):
		self.iface.removePluginMenu("ExtractCentroid",self.action)

	def extract_centroid(self):
		new_layer = QgsVectorLayer("./sampledata/sample_data.shp", "polygons", "ogr")
		if not new_layer:
			print "Layer failed to load!"
		else:
			print "Layer has been loaded"
			layer_shape = QgsMapLayerRegistry.instance().addMapLayers([new_layer])
			for feature in layer_shape.getFeatures():
				feature.geometry().centroid()
			QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('ExtractCentroid', "Extracted Centroid"), QCoreApplication.translate('ExtractCentroid', "Extracted Centroid"))
		return

if __name__ == "__main__":
	pass