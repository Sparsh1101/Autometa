// SPDM-Liscence-Identifier: MIT
pragma experimental ABIEncoderV2;

pragma solidity ^0.6.0;

contract VehicleContract {

    struct OwnerInfo {
        bool exists;
        string fName;
        string lName;
        string aadhar;
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

    mapping(string => OwnerInfo) aadharToOwnerInfo;
    mapping(string => VehicleInfo) uniqueIDToVehicleInfo;
    // mapping(string => VehicleInfo) uniqueIDToVehicleInfo;

    function storeInfo(
        string memory _uniqueID,
        string memory _vehicleNo,
        string memory _modelName,
        string memory _vehicleColor,
        string memory _fName,
        string memory _lName,
        string memory _aadhar,
        string memory _dob,
        string memory _gender,
        string memory _email,
        string memory _mobileNo
    ) public {
        if (uniqueIDToVehicleInfo[_uniqueID].exists == true) {
            if (aadharToOwnerInfo[_aadhar].exists == true) {
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp;
                aadharToOwnerInfo[_aadhar] = OwnerInfo(true, _fName, _lName, _aadhar, _dob, _gender, _email, _mobileNo, temp);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
            }
        } else {
            if (aadharToOwnerInfo[_aadhar].exists == true) {
                string[] memory temp;
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(true, _uniqueID, _vehicleNo, _modelName, _vehicleColor, temp);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp1;
                string[] memory temp2;
                aadharToOwnerInfo[_aadhar] = OwnerInfo(true, _fName, _lName, _aadhar, _dob, _gender, _email, _mobileNo, temp1);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(true, _uniqueID, _vehicleNo, _modelName, _vehicleColor, temp2);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
            }
        }
    }

    function getOwnerInfoFromAadhar(string memory _aadhar) public view returns (
        string memory fName,
        string memory lName,
        string memory aadhar,
        string memory dob,
        string memory gender,
        string memory email,
        string memory mobileNo
        ) {
        return (
            aadharToOwnerInfo[_aadhar].fName,
            aadharToOwnerInfo[_aadhar].lName,
            _aadhar,
            aadharToOwnerInfo[_aadhar].dob,
            aadharToOwnerInfo[_aadhar].gender,
            aadharToOwnerInfo[_aadhar].email,
            aadharToOwnerInfo[_aadhar].mobileNo
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

    function getVehiclesFromAadhar(string memory _aadhar) public view returns (string[] memory) {
        return aadharToOwnerInfo[_aadhar].vehicles;
    }

    function getOwnersFromUniqueID(string memory _uniqueID) public view returns (string[] memory) {
        return uniqueIDToVehicleInfo[_uniqueID].owners;
    }

    function updateOwnerInfo(
        string memory _fName,
        string memory _lName,
        string memory _aadhar,
        string memory _dob,
        string memory _gender,
        string memory _email,
        string memory _mobileNo
        ) public {
        require(
            aadharToOwnerInfo[_aadhar].exists == true,
            "Owner doesn't exist!"
        );
        aadharToOwnerInfo[_aadhar].fName = _fName;
        aadharToOwnerInfo[_aadhar].lName = _lName;
        aadharToOwnerInfo[_aadhar].dob = _dob;
        aadharToOwnerInfo[_aadhar].gender = _gender;
        aadharToOwnerInfo[_aadhar].email = _email;
        aadharToOwnerInfo[_aadhar].mobileNo = _mobileNo;
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

    function isOwner(string memory _aadhar) public view returns (bool) {
        return aadharToOwnerInfo[_aadhar].exists;
    }

    function isVehicle(string memory _uniqueID) public view returns (bool) {
        return uniqueIDToVehicleInfo[_uniqueID].exists;
    }

    // '862525352732'
    // '1'
    // '1', '1', 'Santro', 'Blue', 'Sparsh', 'Gupta', '862525352732', ''01-10-2010', 'Male', 'sparshtgupta@gmail.com', '7426463647'
    // 'Riya', 'Guupta', '862525352732', ''01-10-2011', 'Female', 'sparseefhtgupta@gmail.com', '74264636888'
    // '1', '2', 'Santro2', 'Blue2',
}