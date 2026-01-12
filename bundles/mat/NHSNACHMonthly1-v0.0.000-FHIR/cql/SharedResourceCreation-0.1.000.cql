library SharedResourceCreation version '0.1.000'

include FHIRHelpers version '4.4.000' called FHIRHelpers

using FHIR version '4.0.1'

context Patient

define function "GetIdExtensions"(domainResource DomainResource):
  domainResource.extension E
  where E.url.value = 'http://www.cdc.gov/nhsn/fhirportal/dqm/ig/StructureDefinition/link-original-resource-id-extension'
  return E

define function "GetPatientExtensions"(domainResource DomainResource):
  domainResource.extension E
  where E.url.value = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'
    or E.url.value = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'
    or E.url.value = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex'
    or E.url.value = 'http://www.cdc.gov/nhsn/fhirportal/dqm/ig/StructureDefinition/link-original-resource-id-extension'
  return E

define function "MetaElement"(resource Resource, profileURLs List<FHIR.canonical>):
  resource r
  return FHIR.Meta{
    extension: r.meta.extension,
    versionId: r.meta.versionId,
    lastUpdated: r.meta.lastUpdated,
    profile: profileURLs,
    security: r.meta.security,
    tag: r.meta.tag
  }

define function ConditionStage(stage List<FHIR.Condition.Stage>):
  stage s
  return FHIR.Condition.Stage{
    summary: s.summary,
    assessment: s.assessment,
    type: s.type
  }

define function ConditionEvidence(evidence List<FHIR.Condition.Evidence>):
  evidence e
  return FHIR.Condition.Evidence{
    code: e.code,
    detail: e.detail
  }

define function ConditionResource(condition Condition, profileURLs List<FHIR.canonical>):
  condition c
  return Condition{
    id: FHIR.id {value: 'LCR-' + c.id},
    meta: MetaElement(c, profileURLs),
    extension: c.extension,
    clinicalStatus: c.clinicalStatus,
    verificationStatus: c.verificationStatus,
    category: c.category,
    severity: c.severity,
    code: c.code,
    bodySite: c.bodySite,
    subject: c.subject,
    encounter: c.encounter,
    onset: c.onset,
    abatement: c.abatement,
    recordedDate: c.recordedDate,
    stage: ConditionStage(c.stage),
    evidence: ConditionEvidence(c.evidence),
    note: c.note
  }

define function CoverageClass(class List<FHIR.Coverage.Class>):
  class c
  return FHIR.Coverage.Class{
    value: c.value,
    name: c.name
  }

define function CoverageResource(coverage Coverage, profileURLs List<FHIR.canonical>):
  coverage c
  return Coverage{
    id: FHIR.id{value: 'LCR-' + c.id},
    meta: MetaElement(c, profileURLs),
    extension: c.extension,
    status: c.status,
    type: c.type,
    policyHolder: c.policyHolder,
    subscriber: c.subscriber,
    subscriberId: c.subscriberId,
    beneficiary: c.beneficiary,
    dependent: c.dependent,
    relationship: c.relationship,
    period: c.period,
    payor: c.payor,
    class: CoverageClass(c.class),
    order: c.order,
    network: c.network,
    subrogation: c.subrogation,
    contract: c.contract
  }

define function DiagnosticReportCoding(coding List<Coding>):
  coding c
  return Coding{
    system: c.system,
    version: c.version,
    code: c.code,
    display: c.display,
    userSelected: c.userSelected
  }

define function DiagnosticReportCategory(category List<CodeableConcept>):
  category c
  return CodeableConcept{
    coding: DiagnosticReportCoding(c.coding)
  }

define function DiagnosticReportLabResource(diagnosticReport DiagnosticReport, profileURLs List<FHIR.canonical>):
  diagnosticReport d
  return DiagnosticReport{
    id: FHIR.id{value: 'LCR-' + d.id},
    meta: MetaElement(d, profileURLs),
    extension: d.extension,
    basedOn: d.basedOn,
    status: d.status,
    category: DiagnosticReportCategory(d.category),
    code: d.code,
    subject: d.subject,
    encounter: d.encounter,
    effective: d.effective,
    issued: d.issued,
    performer: d.performer,
    resultsInterpreter: d.resultsInterpreter,
    specimen: d.specimen,
    result: d.result,
    conclusion: d.conclusion,
    conclusionCode: d.conclusionCode
  }

define function EncounterIdentifier(identifier List<FHIR.Identifier>):
  identifier i
  return FHIR.Identifier{
    use: i.use,
    type: i.type,
    system: i.system,
    value: i.value,
    period: i.period
  }

define function EncounterStatusHistory(statusHistory List<FHIR.Encounter.StatusHistory>):
  statusHistory sH
  return FHIR.Encounter.StatusHistory{
    status: sH.status,
    period: sH.period
  }

define function EncounterClassHistory(classHistory List<FHIR.Encounter.ClassHistory>):
  classHistory cH
  return FHIR.Encounter.ClassHistory{
    class: cH.class,
    period: cH.period
  }

/*No longer needed but saving for potential future use
define function EncounterParticipant(participant List<FHIR.Encounter.Participant>):
  participant p
  return FHIR.Encounter.Participant{
    type: p.type,
    period: p.period,
    individual: p.individual
  }*/

define function EncounterDiagnosis(diagnosis List<FHIR.Encounter.Diagnosis>):
  diagnosis d
  return FHIR.Encounter.Diagnosis{
    condition: d.condition,
    use: d.use,
    rank: d.rank
  }

define function EncounterHospitalization(hospitalization FHIR.Encounter.Hospitalization):
  hospitalization h
  return FHIR.Encounter.Hospitalization{
    preAdmissionIdentifier: h.preAdmissionIdentifier,
    origin: h.origin,
    admitSource: h.admitSource,
    reAdmission: h.reAdmission,
    dietPreference: h.dietPreference,
    specialCourtesy: h.specialCourtesy,
    specialArrangement: h.specialArrangement,
    destination: h.destination,
    dischargeDisposition: h.dischargeDisposition
  }

define function EncounterLocation(location List<FHIR.Encounter.Location>):
  location l
  return FHIR.Encounter.Location{
    location: l.location,
    status: l.status,
    physicalType: l.physicalType,
    period: l.period
  }

define function EncounterResource(encounter Encounter, profileURLs List<FHIR.canonical>):
  encounter e
  return Encounter{
    id: FHIR.id{value: 'LCR-' + e.id},
    meta: MetaElement(e, profileURLs),
    extension: e.extension,
    identifier: EncounterIdentifier(e.identifier),
    status: e.status,
    statusHistory: EncounterStatusHistory(e.statusHistory),
    class: e.class,
    classHistory: EncounterClassHistory(e.classHistory),
    type: e.type,
    serviceType: e.serviceType,
    priority: e.priority,
    subject: e.subject,
    period: e.period,
    length: e.length,
    reasonCode: e.reasonCode,
    reasonReference: e.reasonReference,
    diagnosis: EncounterDiagnosis(e.diagnosis),
    account: e.account,
    hospitalization: EncounterHospitalization(e.hospitalization),
    location: EncounterLocation(e.location),
    partOf: e.partOf
  }

define function ObservationLabCoding(coding List<Coding>):
  coding c
  return Coding{
    id: c.id,
    extension: c.extension,
    system: c.system,
    version: c.version,
    code: c.code,
    display: c.display,
    userSelected: c.userSelected
  }

define function ObservationLabCategory(category List<CodeableConcept>):
  category c
  return CodeableConcept{
    coding: ObservationLabCoding(c.coding),
    text: c.text
  }

define function ObservationReferenceRange(referenceRange List<FHIR.Observation.ReferenceRange>):
  referenceRange rR
  return FHIR.Observation.ReferenceRange{
    low: rR.low,
    high: rR.high,
    type: rR.type,
    appliesTo: rR.appliesTo,
    age: rR.age,
    text: rR.text
  }

define function ObservationComponent(component List<FHIR.Observation.Component>):
  component c
  return FHIR.Observation.Component{
    code: c.code,
    value: c.value,
    dataAbsentReason: c.dataAbsentReason,
    interpretation: c.interpretation,
    referenceRange: c.referenceRange
  }

define function ObservationLabResource(observation Observation, profileURLs List<FHIR.canonical>):
  observation o
  return Observation{
    id: FHIR.id {value: 'LCR-' + o.id},
    meta: MetaElement(o, profileURLs),
    extension: o.extension,
    basedOn: o.basedOn,
    partOf: o.partOf,
    status: o.status,
    category: ObservationLabCategory(o.category),
    code: o.code,
    subject: o.subject,
    focus: o.focus,
    encounter: o.encounter,
    effective: o.effective,
    issued: o.issued,
    performer: o.performer,
    value: o.value,
    dataAbsentReason: o.dataAbsentReason,
    interpretation: o.interpretation,
    note: o.note,
    bodySite: o.bodySite,
    method: o.method,
    specimen: o.specimen,
    device: o.device,
    referenceRange: ObservationReferenceRange(o.referenceRange),
    hasMember: o.hasMember,
    derivedFrom: o.derivedFrom,
    component: ObservationComponent(o.component)
  }

define function LocationAddress(address FHIR.Address):
  address a
  return FHIR.Address{
    use: a.use,
    type: a.type,
    text: a.text,
    line: a.line,
    city: a.city,
    district: a.district,
    state: a.state,
    postalCode: a.postalCode,
    country: a.country,
    period: a.period
  }

define function LocationPosition(position FHIR.Location.Position):
  position p
  return FHIR.Location.Position{
    longitude: p.longitude,
    latitude: p.latitude,
    altitude: p.altitude
  }

define function LocationHoursOfOperation(hoursOfOperation List<FHIR.Location.HoursOfOperation>):
  hoursOfOperation hOO
  return FHIR.Location.HoursOfOperation{
    daysOfWeek: hOO.daysOfWeek,
    allDay: hOO.allDay,
    openingTime: hOO.openingTime,
    closingTime: hOO.closingTime
  }

define function LocationResource(location Location, profileURLs List<FHIR.canonical>):
  location l
  return Location{
    id: FHIR.id {value: 'LCR-' + l.id},
    meta: MetaElement(l, profileURLs),
    extension: l.extension,
    status: l.status,
    operationalStatus: l.operationalStatus,
    name: l.name,
    alias: l.alias,
    description: l.description,
    mode: l.mode,
    type: l.type,
    telecom: l.telecom,
    address: LocationAddress(l.address),
    physicalType: l.physicalType,
    position: LocationPosition(l.position),
    managingOrganization: l.managingOrganization,
    partOf: l.partOf,
    hoursOfOperation: LocationHoursOfOperation(l.hoursOfOperation),
    availabilityExceptions: l.availabilityExceptions,
    endpoint: l.endpoint
  }

define function MedicationIngredient(ingredient List<FHIR.Medication.Ingredient>):
  ingredient i
  return FHIR.Medication.Ingredient{
    item: i.item,
    strength: i.strength
  }

define function MedicationBatch(batch FHIR.Medication.Batch):
  batch b
  return FHIR.Medication.Batch{
    lotNumber: b.lotNumber,
    expirationDate: b.expirationDate
  }

define function MedicationResource(medication Medication, profileURLs List<FHIR.canonical>):
  medication m
  return Medication{
    id: FHIR.id {value: 'LCR-' + m.id},
    meta: MetaElement(m, profileURLs),
    extension: m.extension,
    code: m.code,
    status: m.status,
    manufacturer: m.manufacturer,
    form: m.form,
    amount: m.amount,
    ingredient: MedicationIngredient(m.ingredient),
    batch: MedicationBatch(m.batch)
  }

define function MedicationAdministrationPerformer(performer List<FHIR.MedicationAdministration.Performer>):
  performer p
  return FHIR.MedicationAdministration.Performer{
    function: p.function,
    actor: p.actor
  }

define function MedicationAdministrationDosage(dosage FHIR.MedicationAdministration.Dosage):
  dosage d
  return FHIR.MedicationAdministration.Dosage{
    text: d.text,
    site: d.site,
    route: d.route,
    method: d.method,
    dose: d.dose,
    rate: d.rate
  }

define function MedicationAdministrationResource(medicationAdministration MedicationAdministration, profileURLs List<FHIR.canonical>):
  medicationAdministration m
  return MedicationAdministration{
    id: FHIR.id {value: 'LCR-' + m.id},
    meta: MetaElement(m, profileURLs),
    extension: m.extension,
    instantiates: m.instantiates,
    partOf: m.partOf,
    status: m.status,
    statusReason: m.statusReason,
    category: m.category,
    medication: m.medication,
    subject: m.subject,
    context: m.context,
    supportingInformation: m.supportingInformation,
    effective: m.effective,
    performer: MedicationAdministrationPerformer(m.performer),
    reasonCode: m.reasonCode,
    reasonReference: m.reasonReference,
    request: m.request,
    device: m.device,
    note: m.note,
    dosage: MedicationAdministrationDosage(m.dosage),
    eventHistory: m.eventHistory
  }

define function MedicationRequestDoseAndRate(doseAndRate List<FHIR.Dosage.DoseAndRate>):
  doseAndRate dR
  return FHIR.Dosage.DoseAndRate{
    type: dR.type,
    dose: dR.dose,
    rate: dR.rate
  }

define function MedicationRequestDosageInstruction(dosageInstruction List<FHIR.Dosage>):
  dosageInstruction dI
  return FHIR.Dosage{
    text: dI.text,
    patientInstruction: dI.patientInstruction,
    timing: dI.timing,
    asNeeded: dI.asNeeded,
    site: dI.site,
    route: dI.route,
    method: dI.method,
    doseAndRate: MedicationRequestDoseAndRate(dI.doseAndRate)
  }

define function MedicationRequestResource(medicationRequest MedicationRequest, profileURLs List<FHIR.canonical>):
  medicationRequest m
  return MedicationRequest{
    id: FHIR.id {value: 'LCR-' + m.id},
    meta: MetaElement(medicationRequest, profileURLs),
    extension: m.extension,
    status: m.status,
    statusReason: m.statusReason,
    intent: m.intent,
    category: m.category,
    priority: m.priority,
    doNotPerform: m.doNotPerform,
    reported: m.reported,
    medication: m.medication,
    subject: m.subject,
    encounter: m.encounter,
    authoredOn: m.authoredOn,
    requester: m.requester,
    recorder: m.recorder,
    reasonCode: m.reasonCode,
    reasonReference: m.reasonReference,
    instantiatesCanonical: m.instantiatesCanonical,
    instantiatesUri: m.instantiatesUri,
    courseOfTherapyType: m.courseOfTherapyType,
    dosageInstruction: MedicationRequestDosageInstruction(m.dosageInstruction)
  }

/* No longer needed but saving in case it's useful later
define function PatientIdentifier(identifier List<FHIR.Identifier>):
  identifier i
  return FHIR.Identifier{
    id: i.id,
    extension: i.extension,
    use: i.use,
    type: i.type,
    system: i.system,
    value: i.value,
    period: i.period,
    assigner: i.assigner
  }*/

define function PatientName(name List<FHIR.HumanName>):
  name n
  return FHIR.HumanName{
    id: n.id,
    extension: n.extension,
    use: n.use,
    text: n.text,
    family: n.family,
    given: n.given,
    prefix: n.prefix,
    suffix: n.suffix,
    period: n.period
  }

define function PatientTelecom(telecom List<FHIR.ContactPoint>):
  telecom t
  return FHIR.ContactPoint{
    system: t.system,
    value: t.value,
    use: t.use,
    rank: t.rank,
    period: t.period
  }

define function PatientAddress(address List<FHIR.Address>):
  address a
  return FHIR.Address{
    id: a.id,
    extension: a.extension,
    use: a.use,
    type: a.type,
    text: a.text,
    line: a.line,
    city: a.city,
    district: a.district,
    state: a.state,
    postalCode: a.postalCode,
    country: a.country,
    period: a.period
  }

define function PatientContact(contact List<FHIR.Patient.Contact>):
  contact c
  return FHIR.Patient.Contact{
    id: c.id,
    extension: c.extension,
    relationship: c.relationship,
    name: c.name,
    telecom: c.telecom,
    address: c.address,
    gender: c.gender,
    organization: c.organization,
    period: c.period
  }

define function PatientCommunication(communication List<FHIR.Patient.Communication>):
  communication c
  return FHIR.Patient.Communication{
    id: c.id,
    extension: c.extension,
    language: c.language,
    preferred: c.preferred
  }

define function PatientLink(link List<FHIR.Patient.Link>):
  link l
  return FHIR.Patient.Link{
    id: l.id,
    extension: l.extension,
    modifierExtension: l.modifierExtension,
    other: l.other,
    type: l.type
  }

define function PatientResource(patient Patient, profileURLs List<FHIR.canonical>):
  patient p
  return Patient{
    id: FHIR.id{value: 'LCR-' + p.id},
    meta: MetaElement(p, profileURLs),
    extension: GetPatientExtensions(p) union GetIdExtensions(p),
    identifier: p.identifier,
    active: p.active,
    name: PatientName(p.name),
    telecom: PatientTelecom(p.telecom),
    gender: p.gender,
    birthDate: p.birthDate,
    deceased: p.deceased,
    address: PatientAddress(p.address),
    maritalStatus: p.maritalStatus,
    multipleBirth: p.multipleBirth,
    photo: p.photo,
    contact: PatientContact(p.contact),
    communication: PatientCommunication(p.communication),
    generalPractitioner: p.generalPractitioner,
    managingOrganization: p.managingOrganization,
    link: PatientLink(p.link)
  }

define function ProcedurePerformer(performer List<FHIR.Procedure.Performer>):
  performer p
  return FHIR.Procedure.Performer{
    function: p.function,
    actor: p.actor,
    onBehalfOf: p.onBehalfOf
  }

define function ProcedureFocalDevice(device List<FHIR.Procedure.FocalDevice>):
  device d
  return FHIR.Procedure.FocalDevice{
    action: d.action,
    manipulated: d.manipulated
  }

define function ProcedureResource(procedure Procedure, profileURLs List<FHIR.canonical>):
  procedure p
  return Procedure{
    id: FHIR.id {value: 'LCR-' + p.id},
    meta: MetaElement(p, profileURLs),
    extension: p.extension,
    instantiatesCanonical: p.instantiatesCanonical,
    instantiatesUri: p.instantiatesUri,
    basedOn: p.basedOn,
    partOf: p.partOf,
    status: p.status,
    statusReason: p.statusReason,
    category: p.category,
    code: p.code,
    subject: p.subject,
    encounter: p.encounter,
    performed: p.performed,
    recorder: p.recorder,
    asserter: p.asserter,
    performer: ProcedurePerformer(p.performer),
    location: p.location,
    reasonCode: p.reasonCode,
    reasonReference: p.reasonReference,
    bodySite: p.bodySite,
    outcome: p.outcome,
    report: p.report,
    complication: p.complication,
    complicationDetail: p.complicationDetail,
    followUp: p.followUp,
    note: p.note,
    focalDevice: ProcedureFocalDevice(p.focalDevice),
    usedReference: p.usedReference,
    usedCode: p.usedCode
  }

define function ServiceRequestResource(serviceRequest ServiceRequest, profileURLs List<FHIR.canonical>):
  serviceRequest sR
  return ServiceRequest{
    id: FHIR.id {value: 'LCR-' + sR.id},
    meta: MetaElement(sR, profileURLs),
    extension: sR.extension,
    instantiatesCanonical: sR.instantiatesCanonical,
    instantiatesUri: sR.instantiatesUri,
    basedOn: sR.basedOn,
    replaces: sR.replaces,
    requisition: sR.requisition,
    status: sR.status,
    intent: sR.intent,
    category: sR.category,
    priority: sR.priority,
    doNotPerform: sR.doNotPerform,
    code: sR.code,
    orderDetail: sR.orderDetail,
    quantity: sR.quantity,
    subject: sR.subject,
    encounter: sR.encounter,
    occurrence: sR.occurrence,
    asNeeded: sR.asNeeded,
    authoredOn: sR.authoredOn,
    requester: sR.requester,
    performerType: sR.performerType,
    performer: sR.performer,
    locationCode: sR.locationCode,
    locationReference: sR.locationReference,
    reasonCode: sR.reasonCode,
    reasonReference: sR.reasonReference,
    insurance: sR.insurance,
    supportingInfo: sR.supportingInfo,
    specimen: sR.specimen,
    bodySite: sR.bodySite,
    note: sR.note,
    patientInstruction: sR.patientInstruction,
    relevantHistory: sR.relevantHistory
  }

define function SpecimenCollection(collection FHIR.Specimen.Collection):
  collection c
  return FHIR.Specimen.Collection{
    collector: c.collector,
    collected: c.collected,
    "duration": c."duration",
    quantity: c.quantity,
    method: c.method,
    bodySite: c.bodySite,
    fastingStatus: c.fastingStatus
  }

define function SpecimenProcessing(processing List<FHIR.Specimen.Processing>):
  processing p
  return FHIR.Specimen.Processing{
    description: p.description,
    procedure: p.procedure,
    additive: p.additive,
    time: p.time
  }

define function SpecimenContainer(container List<FHIR.Specimen.Container>):
  container c
  return FHIR.Specimen.Container{
    description: c.description,
    type: c.type,
    capacity: c.capacity,
    specimenQuantity: c.specimenQuantity,
    additive: c.additive
  }

define function SpecimenResource(specimen Specimen, profileURLs List<FHIR.canonical>):
  specimen s
  return Specimen{
    id: FHIR.id {value: 'LCR-' + s.id},
    meta: MetaElement(s, profileURLs),
    extension: s.extension,
    identifier: s.identifier,
    accessionIdentifier: s.accessionIdentifier,
    status: s.status,
    type: s.type,
    subject: s.subject,
    receivedTime: s.receivedTime,
    parent: s.parent,
    request: s.request,
    collection: SpecimenCollection(s.collection),
    processing: SpecimenProcessing(s.processing),
    container: SpecimenContainer(s.container),
    condition: s.condition,
    note: s.note
  }

define function "OperationOutcomeResource"(errorId String, resourceId FHIR.id, message String):
  OperationOutcome{
      id: FHIR.id{value: errorId},
      issue: {
          FHIR.OperationOutcome.Issue{
          severity: FHIR.IssueSeverity{value: 'error'},
          code: FHIR.IssueType{value: 'exception'},
          details: 
              FHIR.CodeableConcept{
                  coding: {
                      Coding{
                      system: uri{value: 'https://lantanagroup.com/validation-error'},
                      code: code{value: 'Error'},
                      display: string{value: 'Resource ' + resourceId + ' failed validation: ' + message}
                      }
                  }
              }
          }
      }
  }