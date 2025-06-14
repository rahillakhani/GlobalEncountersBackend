from typing import Union, Optional

# Special registration IDs that allow unlimited meals
# Format: FB001-80017860

SPECIAL_REGISTRATIONS = {
    "FB001-80017860": 80017860,
    "FB002-80027860": 80027860,
    "FB003-80037860": 80037860,
    "FB004-80047860": 80047860,
    "FB005-80057860": 80057860,
    "FB006-80067860": 80067860,
    "FB007-80077860": 80077860,
    "FB008-80087860": 80087860,
    "FB009-80097860": 80097860,
    "FB010-80107860": 80107860,
    "FB011-80117860": 80117860,
    "FB012-80127860": 80127860,
    "FB013-80137860": 80137860,
    "FB014-80147860": 80147860,
    "FB015-80157860": 80157860,
    "FB016-80167860": 80167860,
    "FB017-80177860": 80177860,
    "FB018-80187860": 80187860,
    "FB019-80197860": 80197860,
    "FB020-80207860": 80207860,
    "FB021-80217860": 80217860,
    "FB022-80227860": 80227860,
    "FB023-80237860": 80237860,
    "FB024-80247860": 80247860,
    "FB025-80257860": 80257860,
    "FB026-80267860": 80267860,
    "FB027-80277860": 80277860,
    "FB028-80287860": 80287860,
    "FB029-80297860": 80297860,
    "FB030-80307860": 80307860,
    "FB031-80317860": 80317860,
    "FB032-80327860": 80327860,
    "FB033-80337860": 80337860,
    "FB034-80347860": 80347860
}

def is_special_registration(registration_id: Union[str, int]) -> bool:
    """
    Check if a registration ID is in the special list that allows unlimited meals
    
    Args:
        registration_id: Can be either string (e.g., "FB005-80057860") or int (e.g., 80057860)
        
    Returns:
        bool: True if the registration ID is in the special list
    """
    if isinstance(registration_id, str):
        # Check if it's in the exact format
        if registration_id in SPECIAL_REGISTRATIONS:
            return True
        # Extract the numeric part as fallback
        numeric_part = ''.join(filter(str.isdigit, registration_id))
        if numeric_part:
            registration_id = int(numeric_part)
    
    return registration_id in SPECIAL_REGISTRATIONS.values()

def get_special_registration_code(registration_id: Union[str, int]) -> Optional[str]:
    """
    Get the special registration code (e.g., "FB005-80057860") for a given registration ID
    
    Args:
        registration_id: Can be either string or int
        
    Returns:
        Optional[str]: The special registration code if found, None otherwise
    """
    if isinstance(registration_id, str):
        # Check if it's in the exact format
        if registration_id in SPECIAL_REGISTRATIONS:
            return registration_id
        # Extract the numeric part as fallback
        numeric_part = ''.join(filter(str.isdigit, registration_id))
        if numeric_part:
            registration_id = int(numeric_part)
    
    # Find the code for this registration ID
    for code, id_value in SPECIAL_REGISTRATIONS.items():
        if id_value == registration_id:
            return code
    
    return None 