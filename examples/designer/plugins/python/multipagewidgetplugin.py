#============================================================================#
# PySide port of the designer/containerextension example from Qt v4.x         #
#----------------------------------------------------------------------------#
from PySide import QtCore, QtGui, QtDesigner
import sip
from multipagewidget import PyMultiPageWidget

Q_TYPEID = {'QPyDesignerContainerExtension':     'com.trolltech.Qt.Designer.Container',
            'QPyDesignerPropertySheetExtension': 'com.trolltech.Qt.Designer.PropertySheet',
            'QPyDesignerTaskMenuExtension':      'com.trolltech.Qt.Designer.TaskMenu',
            'QPyDesignerMemberSheetExtension':   'com.trolltech.Qt.Designer.MemberSheet'}

#============================================================================#
# ContainerExtension                                                         #
#----------------------------------------------------------------------------#
class MultiPageWidgetContainerExtension(QtDesigner.QPyDesignerContainerExtension):
    def __init__(self, widget, parent=None):
        QtDesigner.QPyDesignerContainerExtension.__init__(self, parent)
        self._widget = widget
            
    def addWidget(self, widget):
        self._widget.addPage(widget)
    
    def count(self):
        return self._widget.count()
    
    def currentIndex(self):
        return self._widget.getCurrentIndex()
    
    def insertWidget(self, index, widget):
        self._widget.insertPage(index, widget)
    
    def remove(self, index):
        self._widget.removePage(index)
    
    def setCurrentIndex(self, index):
        self._widget.setCurrentIndex(index)
    
    def widget(self, index):
        return self._widget.widget(index)
    

#============================================================================#
# ExtensionFactory                                                           #
#----------------------------------------------------------------------------#
class MultiPageWidgetExtensionFactory(QtDesigner.QExtensionFactory):
    def __init__(self, parent=None):
        QtDesigner.QExtensionFactory.__init__(self, parent)

    def createExtension(self, obj, iid, parent):
        if iid != Q_TYPEID['QPyDesignerContainerExtension']:
            return None
        if isinstance(obj, PyMultiPageWidget):
            return MultiPageWidgetContainerExtension(obj, parent)
        return None


#============================================================================#
# CustomWidgetPlugin                                                         #
#----------------------------------------------------------------------------#
class MultiPageWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):    
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self, parent)
        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        manager = formEditor.extensionManager()
        if manager:
            self.factory = MultiPageWidgetExtensionFactory(manager)
            manager.registerExtensions(self.factory, Q_TYPEID['QPyDesignerContainerExtension'])
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        widget = PyMultiPageWidget(parent)
        self.connect(widget, QtCore.SIGNAL('currentIndexChanged(int)'), self.currentIndexChanged)
        self.connect(widget, QtCore.SIGNAL('pageTitleChanged(const QString &)'), self.pageTitleChanged)
        return widget

    def name(self):
        return "PyMultiPageWidget"

    def group(self):
        return "PyQt Examples"

    def icon(self):
        return QtGui.QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return True

    def domXml(self):
        return ('<widget class="PyMultiPageWidget" name="multipagewidget">'
                '  <widget class="QWidget" name="page" />'
                '</widget>')

    def includeFile(self):
        return "multipagewidget"

    @QtCore.pyqtSignature("int")
    def currentIndexChanged(self, index):
        widget = self.sender()
        if widget and isinstance(widget, PyMultiPageWidget):
            form = QtDesigner.QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                form.emitSelectionChanged()

    @QtCore.pyqtSignature("const QString &")
    def pageTitleChanged(self, title):
        widget = self.sender()
        if widget and isinstance(widget, PyMultiPageWidget):
            page = widget.widget(widget.getCurrentIndex())
            form = QtDesigner.QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                editor = form.core()
                manager = editor.extensionManager()
                sheet = manager.extension(page, Q_TYPEID['QPyDesignerPropertySheetExtension'])
                # This explicit cast is necessary here
                sheet = sip.cast(sheet, QtDesigner.QPyDesignerPropertySheetExtension)
                propertyIndex = sheet.indexOf('windowTitle')
                sheet.setChanged(propertyIndex, True)

#============================================================================#
# EOF                                                                        #
#----------------------------------------------------------------------------#
