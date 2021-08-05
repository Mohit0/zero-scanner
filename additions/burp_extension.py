from burp import IBurpExtender, ITab 
from javax import swing
from java.awt import BorderLayout
import sys

try:
    from exceptions_fix import FixBurpExceptions
except ImportError:
    pass

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        sys.stdout = callbacks.getStdout()
        self.callbacks = callbacks
        self.callbacks.setExtensionName("Mobile Application Security Framework")
        self.tab = swing.JPanel(BorderLayout())

        tabbedPane = swing.JTabbedPane()
        self.tab.add("Center", tabbedPane);

        firstTab = swing.JPanel()
        firstTab.layout = BorderLayout()
        tabbedPane.addTab("Main", firstTab)

        textPanel = swing.JPanel()
        boxVertical = swing.Box.createVerticalBox()

        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("  Path to Mobile Application :   "))
        boxHorizontal.add(swing.JTextArea('', 1, 50))

        boxVertical.add(boxHorizontal)

        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JButton('Scan', actionPerformed=self.handleButtonClick))

        boxVertical.add(boxHorizontal)

        boxHorizontal = swing.Box.createHorizontalBox()
        self.textArea = swing.JTextArea('Output Here', 20, 100)
        self.textArea.setLineWrap(True)
        scroll = swing.JScrollPane(self.textArea)
        boxHorizontal.add(scroll)

        boxVertical.add(boxHorizontal)
        textPanel.add(boxVertical)

        firstTab.add(textPanel, "West")


        secondTab = swing.JPanel()
        secondTab.layout = BorderLayout()
        tabbedPane.addTab("Config", secondTab)

        textPanel = swing.JPanel()
        boxVertical = swing.Box.createVerticalBox(

        boxHorizontal = swing.Box.createHorizontalBox()
        boxHorizontal.add(swing.JLabel("  Path to MobSF Folder :   "))
        boxHorizontal.add(swing.JTextArea('', 1, 50))

        boxVertical.add(boxHorizontal)
        textPanel.add(boxVertical)

        secondTab.add(textPanel, "West")


        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        return


    # Implement ITab
    def getTabCaption(self):
        """Return the text to be displayed on the tab"""
        return "MobSF"
    
    def getUiComponent(self):
        """Passes the UI to burp"""
        return self.tab

    def handleButtonClick(self, event):
        buttonText = event.source.text
        if buttonText == "Scan":
            self.scanning()
        else:
            print buttonText

    #def scanning(self):
        #self.b64EncField.text = base64.b64encode(self.textArea.text)
        #self.urlEncField.text = urllib.quote(self.textArea.text)
        #self.asciiHexEncField.text = binascii.hexlify(self.textArea.text)
        #self.htmlEncField.text = cgi.escape(self.textArea.text)
        #self.jsEncField.text = json.dumps(self.textArea.text)




try:
    FixBurpExceptions()
except:
    pass
