// SPDM-Liscence-Identifier: MIT
pragma experimental ABIEncoderV2;

pragma solidity ^0.6.0;

contract VehicleContract {

    struct OwnerInfo {
        bool exists;
        string fName;
        string lName;
        string adhaar;
        string dob;
        string gender;
        string email;
        string mobileNo;
        string[] vehicles;
    }

    struct VehicleInfo {
        bool exists;
        string uniqueID;
        string vehicleNo;
        string modelName;
        string vehicleColor;
        string[] owners;
    }

    mapping(string => OwnerInfo) adhaarToOwnerInfo;
    mapping(string => VehicleInfo) uniqueIDToVehicleInfo;
    // mapping(string => VehicleInfo) uniqueIDToVehicleInfo;

    function storeInfo(
        string memory _uniqueID,
        string memory _vehicleNo,
        string memory _modelName,
        string memory _vehicleColor,
        string memory _fName,
        string memory _lName,
        string memory _adhaar,
        string memory _dob,
        string memory _gender,
        string memory _email,
        string memory _mobileNo
    ) public {
        if (uniqueIDToVehicleInfo[_uniqueID].exists == true) {
            if (adhaarToOwnerInfo[_adhaar].exists == true) {
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_adhaar);
                adhaarToOwnerInfo[_adhaar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp;
                adhaarToOwnerInfo[_adhaar] = OwnerInfo(true, _fName, _lName, _adhaar, _dob, _gender, _email, _mobileNo, temp);
                adhaarToOwnerInfo[_adhaar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_adhaar);
            }
        } else {
            if (adhaarToOwnerInfo[_adhaar].exists == true) {
                string[] memory temp;
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(true, _uniqueID, _vehicleNo, _modelName, _vehicleColor, temp);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_adhaar);
                adhaarToOwnerInfo[_adhaar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp1;
                string[] memory temp2;
                adhaarToOwnerInfo[_adhaar] = OwnerInfo(true, _fName, _lName, _adhaar, _dob, _gender, _email, _mobileNo, temp1);
                adhaarToOwnerInfo[_adhaar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(true, _uniqueID, _vehicleNo, _modelName, _vehicleColor, temp2);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_adhaar);
            }
        }
    }

    function getOwnerInfoFromAdhaar(string memory _adhaar) public view returns (
        string memory fName,
        string memory lName,
        string memory adhaar,
        string memory dob,
        string memory gender,
        string memory email,
        string memory mobileNo
        ) {
        return (
            adhaarToOwnerInfo[_adhaar].fName,
            adhaarToOwnerInfo[_adhaar].lName,
            _adhaar,
            adhaarToOwnerInfo[_adhaar].dob,
            adhaarToOwnerInfo[_adhaar].gender,
            adhaarToOwnerInfo[_adhaar].email,
            adhaarToOwnerInfo[_adhaar].mobileNo
        );
    }

    function getVehicleInfoFromUniqueID(string memory _uniqueID) public view returns (
        string memory uniqueID,
        string memory vehicleNo,
        string memory modelName,
        string memory vehicleColor
        ) { 
        return (
            _uniqueID,
            uniqueIDToVehicleInfo[_uniqueID].vehicleNo,
            uniqueIDToVehicleInfo[_uniqueID].modelName,
            uniqueIDToVehicleInfo[_uniqueID].vehicleColor
        );
    }

    function getVehiclesFromAdhaar(string memory _adhaar) public view returns (string[] memory) {
        return adhaarToOwnerInfo[_adhaar].vehicles;
    }

    function getOwnersFromUniqueID(string memory _uniqueID) public view returns (string[] memory) {
        return uniqueIDToVehicleInfo[_uniqueID].owners;
    }

    function updateOwnerInfo(
        string memory _fName,
        string memory _lName,
        string memory _adhaar,
        string memory _dob,
        string memory _gender,
        string memory _email,
        string memory _mobileNo
        ) public {
        require(
            adhaarToOwnerInfo[_adhaar].exists == true,
            "Owner doesn't exist!"
        );
        adhaarToOwnerInfo[_adhaar].fName = _fName;
        adhaarToOwnerInfo[_adhaar].lName = _lName;
        adhaarToOwnerInfo[_adhaar].dob = _dob;
        adhaarToOwnerInfo[_adhaar].gender = _gender;
        adhaarToOwnerInfo[_adhaar].email = _email;
        adhaarToOwnerInfo[_adhaar].mobileNo = _mobileNo;
    }

    function updateVehicleInfo(
        string memory _uniqueID,
        string memory _vehicleNo,
        string memory _modelName,
        string memory _vehicleColor
        ) public {
        require(
            uniqueIDToVehicleInfo[_uniqueID].exists == true,
            "Vehicle doesn't exist!"
        );
        uniqueIDToVehicleInfo[_uniqueID].vehicleNo = _vehicleNo;
        uniqueIDToVehicleInfo[_uniqueID].modelName = _modelName;
        uniqueIDToVehicleInfo[_uniqueID].vehicleColor = _vehicleColor;
    }

    // '862525352732'
    // '1'
    // '1', '1', 'Santro', 'Blue', 'Sparsh', 'Gupta', '862525352732', ''01-10-2010', 'Male', 'sparshtgupta@gmail.com', '7426463647'
    // 'Riya', 'Guupta', '862525352732', ''01-10-2011', 'Female', 'sparseefhtgupta@gmail.com', '74264636888'
    // '1', '2', 'Santro2', 'Blue2',
}