#!/usr/bin/python

from QtMobility.Messaging import *
from PySide.QtCore import *
import sys

app = QCoreApplication(sys.argv)

print "Querying messages..."

# Match all messages whose status field includes the Incoming flag
filter = QMessageFilter.byStatus(QMessage.Incoming)

# Order the matching results by their reception timestamp, in descending order
sortOrder = QMessageSortOrder.byReceptionTimeStamp(Qt.DescendingOrder)

# Acquire a handle to the message manager
manager = QMessageManager()

# Find the matching message IDs, limiting our results to a managable number
matchingIds = manager.queryMessages(filter, sortOrder, 100)

n = 0

# Retrieve each message and print requested details
for id in matchingIds:
    message = manager.message(id)

    if manager.error() == QMessageManager.NoError:
        result = []

        if len(sys.argv) < 2:
            # Default to printing only the subject
            result.append(message.subject())
        else:
            # Extract the requested data items from this message
            args = sys.argv
            for arg in args[1:]:
                if arg == "subject":
                    result.append(message.subject())
                elif arg == "date":
                    result.append(message.date().toLocalTime().toString())
                elif arg == "receivedDate":
                    result.append(message.receivedDate().toLocalTime().toString())
                elif arg == "size":
                    result.append(str(message.size()))
                elif arg == "priority":
                    if message.priority() == QMessage.HighPriority:
                        result.append("High")
                    elif message.priority() == QMessage.LowPriority:
                        result.append("Low")
                    else:
                        result.append("Normal")
                elif (arg == "to") or (arg == "cc") or (arg == "bcc"):
                    addresses = []
                    dest = []
                    if arg == "to":
                        dest = message.to()
                    elif arg == "cc":
                        dest = message.cc()
                    else:
                        dest = message.bcc()
                    for addr in dest:
                        addresses.append(addr.addressee())
                    result.append(",".join(addresses))
                elif arg == "from":
                    result.append(message.from_().addressee())
                elif arg == "type":
                    result.append(message.contentType() + '/' + message.contentSubType())
                elif arg == "body":
                    result.append(message.find(message.bodyId()).textContent())
                elif arg == "attachments":
                    fileNames = []
                    for id in message.attachmentIds():
                        fileNames.append(message.find(id).suggestedFileName())
                    result.append(",".join(fileNames))

        print(str(++n) + '\t' + "\t".join(result))

if len(matchingIds) == 0:
    print "No matching messages!"
