# -*- coding: utf-8 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os


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
		dir_path = os.path.dirname(os.path.realpath(__file__))
		new_layer = QgsVectorLayer(dir_path+"/sampledata/sample_data.shp", "polygons", "ogr")
		if not new_layer:
			print "Layer failed to load!"
		else:
			print "Layer has been loaded"
			new_layer.isValid()
			epsg = new_layer.crs().postgisSrid()
			uri = "Point?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
			mem_layer = QgsVectorLayer(uri,'point','memory')
			prov = mem_layer.dataProvider()
			i = 0
			features = {}
			for f in new_layer.getFeatures():
				feat = QgsFeature()
				point = f.geometry().centroid().asPoint()
				features["code"] = f["code"]
				features["X"] = point[0]
				features["Y"] = point[1]
				print(features)
				feat.setAttributes([i])
				feat.setGeometry(QgsGeometry.fromPoint(point))
				prov.addFeatures([feat])
				i += 1
			QgsMapLayerRegistry.instance().addMapLayer(new_layer)
			QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
			QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('ExtractCentroid', "Extracted Centroid"), QCoreApplication.translate('ExtractCentroid', "Extracted Centroid"))
		return

if __name__ == "__main__":
	pass