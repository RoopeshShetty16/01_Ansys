# Common contact settings
DEFAULT_CONTACT_FORMULATION = ContactFormulation.AugmentedLagrange
DEFAULT_TRIM_CONTACT = ContactTrimType.Off
DEFAULT_INTERFACE_TREATMENT = ContactInitialEffect.AddOffsetNoRamping

def create_contact(
    body_1, body_2, contact_type, tolerance_value=1e-1, pinball_radius=5,
    contact_formulation=DEFAULT_CONTACT_FORMULATION,
    trim_contact=DEFAULT_TRIM_CONTACT,
    interface_treatment=DEFAULT_INTERFACE_TREATMENT
):
    """
    Creates a contact between two bodies with specified contact type and properties.

    Parameters:
        body_1 (str): Name of the first body.
        body_2 (str): Name of the second body.
        contact_type (ContactType): Type of contact (Frictional, Bonded, etc.).
        tolerance_value (float): Contact tolerance in mm (default: 0.1).
        pinball_radius (float): Pinball radius in mm (default: 5).
        contact_formulation (enum): Contact formulation type (default: Augmented Lagrange).
        trim_contact (enum): Trim contact type (default: Off).
        interface_treatment (enum): Interface treatment type (default: AddOffsetNoRamping).
    """
    # Retrieve location IDs
    NS1 = list(DataModel.GetObjectsByName(body_1)[0].Location.Ids)
    NS2 = list(DataModel.GetObjectsByName(body_2)[0].Location.Ids)
    ids = NS1 + NS2

    # Create connection group
    connections = Model.Connections
    connection_group = connections.AddConnectionGroup()
    
    sm = ExtAPI.SelectionManager
    smInfo = sm.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    smInfo.Ids = ids
    connection_group.Location = smInfo
    connection_group.ToleranceType = ContactToleranceType.Value
    connection_group.ToleranceValue = Quantity(tolerance_value, 'mm')
    connection_group.Name = str(body_1) + " _to_ " + str(body_2)

    # Generate contacts automatically
    connection_group.CreateAutomaticConnections()
    contacts = connection_group.Children

    # Apply contact settings
    for contact in contacts:
        contact.ContactType = contact_type
        contact.ContactFormulation = contact_formulation
        contact.TrimContact = trim_contact
        contact.PinballRegion = ContactPinballType.Radius
        contact.PinballRadius = Quantity(pinball_radius, "mm")
        contact.InterfaceTreatment = interface_treatment
        contact.Behavior = ContactBehavior.Asymmetric
        contact.RenameBasedOnDefinition()

        # Set friction coefficient if contact type is frictional
        if contact_type == ContactType.Frictional:
            contact.FrictionCoefficient = 0.2


# Wrapper functions with predefined properties
def create_Frictional_contact(body_1, body_2, tolerance_value=1e-1):
    create_contact(body_1, body_2, ContactType.Frictional, tolerance_value)

def create_Bonded_contact(body_1, body_2, tolerance_value=1e-1):
    create_contact(body_1, body_2, ContactType.Bonded, tolerance_value)

def create_Frictionless_contact(body_1, body_2, tolerance_value=1e-1):
    create_contact(body_1, body_2, ContactType.Frictionless, tolerance_value)

def create_NoSeparation_contact(body_1, body_2, tolerance_value=1e-1):
    create_contact(body_1, body_2, ContactType.NoSeparation, tolerance_value)
    
### Example Usage
create_Frictional_contact("Cooler NS", "WPC", tolerance_value=1e-1)
create_Bonded_contact("Cooler NS", "WPC", tolerance_value=1e-1)
create_Frictionless_contact("Cooler NS", "WPC", tolerance_value=1e-1)
create_NoSeparation_contact("Cooler NS", "WPC", tolerance_value=1e-1)
