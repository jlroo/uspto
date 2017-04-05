#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 16:25:18 2017

@author: jlroo
"""

import xml.etree.ElementTree as ET
import zipfile
import bz2
import gzip

def openUSPTO(path):
    src = {"path":path,"type":""}
    compression = path[-4:] in (".zip",".tar",".gz",".bz2")
    if compression == False:
        if path[-4:].lower in (".zip",".tar"):
            raise ValueError("Supported compressions gzip, bz2 or bytes data")
        else:
            ptoFile = open(path)
            src["type"] = "xml"
    else:
        src["type"] = "compressed"
        if path[-3:] == ".gz":
            ptoFile = gzip.open(path)
            ptoFile = ptoFile.read()
        elif path[-4:] == ".zip":
            ptoFile = zipfile.ZipFile(path)
            ptoFile = ptoFile.open(ptoFile.namelist()[0])
            ptoFile = ptoFile.read()
        elif path[-4:] == ".bz2":
            ptoFile = bz2.BZ2File(path,'rb')
            ptoFile = ptoFile.read()
        else:
            raise ValueError("Supported files zip,gzip,bz2, uncompress bytes file. \
                              For uncompressed files change compression flag to False.")
    return usptoData(ptoFile,src)

def getDetails(root):
    details = {k.tag:k.text for k in root.getchildren()}
    for info in root.getchildren():
        details.update({k.tag:k.text for k in info})
        if info.getchildren()!=[]:
            for segments in info.getchildren():
                details.update({k.tag:k.text for k in segments})
                if info.getchildren()!=[]:
                    for keys in segments.getchildren():
                        details.update({k.tag:k.text for k in keys})
                        details['case-files-vol'] = str(len(keys.findall("case-file")))
    details = {k:v for k,v in details.items() if '\n' not in v}
    return details

def getFileHeader(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    case_file_header = {}
    for case in casefiles:
        serial_no = int(case.find('serial-number').text)
        case_file_header[serial_no] = {'serial-number':serial_no}
        case_file_header[serial_no].update({ e.tag:e.text for e in case.find('case-file-header').getchildren()})
    return case_file_header

def getFileEvent(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    case_file_event = {}
    for case in casefiles:
        event_statements = case.find('case-file-event-statements')
        if event_statements != None:
            serial_no = int(case.find('serial-number').text)
            case_file_event[serial_no] = {}
            event = {'serial-number':serial_no}
            events = event_statements.findall('case-file-event-statement')
            for i,entry in enumerate(events):
                event.update({e.tag:e.text for e in entry})
                case_file_event[serial_no][i] = event.copy() 
    return case_file_event

def getFileStatements(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    case_file_statements = {}
    for case in casefiles:
        statements = case.find('case-file-statements')
        if statements != None:
            serial_no = int(case.find('serial-number').text)
            case_file_statements[serial_no] = {}
            statement = {'serial-number':serial_no}
            entries = statements.findall('case-file-statement')
            for i,item in enumerate(entries):
                statement.update({e.tag:e.text for e in item})
                case_file_statements[serial_no][i]= statement.copy()
    return case_file_statements

def getClassifications(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    classifications = {}
    for case in casefiles:
        case_classifications = case.find('classifications')
        if case_classifications != None:
            serial_no = int(case.find('serial-number').text)
            classifications[serial_no] = {}
            entries = case_classifications.findall('classification')
            for i,item in enumerate(entries):
                classification = {e.tag:e.text for e in item}
                us_code = item.findall('us-code')
                intl_code = item.findall('international-code')
                if us_code != []:
                    classification['us-code']= ','.join([i.text for i in us_code])
                if intl_code != []:
                    classification['international-code'] = ','.join([i.text for i in intl_code])
                    classification['serial-number'] = serial_no
                classifications[serial_no][i] = classification.copy()
    return classifications

def getClassificationCodes(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    codes = {}
    for case in casefiles:
        case_classifications = case.find('classifications')
        if case_classifications != None:
            serial_no = int(case.find('serial-number').text)
            codes[serial_no] = {}
            case_codes = {'serial-number':serial_no}
            entries = case_classifications.findall('classification')
            for i,item in enumerate(entries):
                case_codes['us-code'] = ','.join([i.text for i in item.findall('us-code')])
                case_codes['international-code'] = ','.join([i.text for i in item.findall('international-code')])
                codes[serial_no][i] = case_codes.copy()
    return codes

def getCorrespondent(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    correspondent = {}
    for case in casefiles:
        entries = case.find('correspondent')
        serial_no = int(case.find('serial-number').text)
        if entries != None:
            correspondent[serial_no] = {'serial-number':serial_no}
            correspondent[serial_no].update({e.tag:e.text for e in entries})
    return correspondent

def getFileOwners(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    case_file_owners = {}
    for case in casefiles:
        case_owners = case.find('case-file-owners')
        if case_owners != None:
            serial_no = int(case.find('serial-number').text)
            case_file_owners[serial_no] = {}
            owners = {'serial-number':serial_no}
            entries = case_owners.findall('case-file-owner')
            for i,item in enumerate(entries):
                owners.update({e.tag:e.text for e in item})
                if item.find('nationality')!=None:
                    owners['nationality'] = {e.tag:e.text for e in item.find('nationality')}
                case_file_owners[serial_no][i]=owners.copy()
    return case_file_owners

def getDesignSearch(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    design_searches = {}
    for case in casefiles:
        searches = case.find('design-searches')
        if searches != None:
            serial_no = int(case.find('serial-number').text)
            design_searches[serial_no] = {}
            search = {'serial-number':serial_no}
            entries = searches.findall('design-search')
            for i,item in enumerate(entries):
                search.update({e.tag:e.text for e in item})
                design_searches[serial_no][i]=search.copy()
    return design_searches

def getPriorApplications(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file"  )
    prior_applications = {}
    for case in casefiles:
        registration = case.find('prior-registration-applications')
        if registration != None:
            serial_no = int(case.find('serial-number').text)
            prior_applications[serial_no] = {}
            prior = {e.tag:e.text for e in registration}
            entries = registration.findall('prior-registration-application')
            prior['prior-registration-application'] = len(entries)
            prior['serial-number'] = serial_no
            for i,item in enumerate(entries):
                prior.update({e.tag:e.text for e in item})
                prior_applications[serial_no][i]= prior.copy()
    return prior_applications

def getForeignApplications(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file")
    foreign_applications = {}
    for case in casefiles:
        applications = case.find('foreign-applications')
        if applications != None:
            serial_no = int(case.find('serial-number').text)
            foreign_applications[serial_no] = {}
            foreign = {'serial-number':serial_no}
            entries = applications.findall('foreign-application')
            for i,item in enumerate(entries):
                foreign.update({e.tag:e.text for e in item})
                foreign_applications[serial_no][i] = foreign.copy()
    return foreign_applications

def getMadridFiling(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file")
    madrid_international = {}
    for case in casefiles:
        requests = case.find('madrid-international-filing-requests')
        if requests != None:
            records = requests.find('madrid-international-filing-record')
            serial_no = int(case.find('serial-number').text)
            madrid_international[serial_no] = {}
            madrid_filing = {'serial-number':serial_no}
            madrid_filing.update({e.tag:e.text for e in records})
            madrid_filing.pop('madrid-history-events')
            madrid_filing['madrid-history-events'] = len(records.find('madrid-history-events').findall('madrid-history-event'))
            madrid_international[serial_no] = madrid_filing.copy()
    return madrid_international

def getMadridEvents(root):
    segments = root.find("application-information").find("file-segments")
    casefiles = segments.find("action-keys").findall("case-file")
    madrid_events = {}
    for case in casefiles:
        requests = case.find('madrid-international-filing-requests')
        if requests != None:
            records = requests.find('madrid-international-filing-record')
            serial_no = int(case.find('serial-number').text)
            madrid_events[serial_no] = {}
            madrid_event = {'serial-number':serial_no}
            events = records.find('madrid-history-events').findall('madrid-history-event')
            for i,entry in enumerate(events):
                madrid_event.update({e.tag:e.text for e in entry})
                madrid_events[serial_no][i] = madrid_event.copy()
    return madrid_events

def write_csv(data,outFile):
    with open(outFile,'wb') as pto:
        case = next(data)
        header = b','.join([k.replace("-","_").encode() for k in case.keys()])+ b'\n'
        values = b','.join([e.encode() for e in case.values()])+ b'\n'
        pto.write(header)
        pto.write(values)
        for nodes in data:
            pto.write(b','.join([e.encode() for e in nodes.values()])+ b'\n')

class usptoData:
    def __init__(self,ptoFile,src):
        self.data = ptoFile
        self.path = src["path"]
        self.fileType = src["type"]

    def getroot(self):
        if self.fileType == "compressed":
            self.root = ET.fromstring(self.data)
        else:
            tree = ET.parse(self.data)
            self.root = tree.getroot()
        return self.root