import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
	width: 600
	height: 600
	visible: true
	title: "Scan QR code to connect"
	
	ColumnLayout {
	anchors.fill: parent
	anchors.margins: 20
	spacing: 0

		Image {
			id: qrCodeImage
			source: "qr.png"
			Layout.alignment: Qt.AlignHCenter
			fillMode: Image.PreserveAspectFit
			Layout.preferredWidth: 500
			Layout.preferredHeight: 500
			smooth: false
		}

        Text {
			id: text
			text: "This QR links to the web interface. Scan it from a device in the same network"
			font.pixelSize: 15
			horizontalAlignment: Text.AlignHCenter
			wrapMode: Text.Wrap
			Layout.alignment: Qt.AlignHCenter
		}
	}
}
