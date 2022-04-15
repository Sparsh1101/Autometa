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
        string[] vehicles;
        OwnerInfo2 ownerInfo2;
    }

    struct OwnerInfo2 {
        string mobileNo;
        string email;
        string userId;
    }

    struct VehicleInfo {
        bool exists;
        string uniqueID;
        string vehicleNo;
        string modelName;
        string vehicleColor;
        string[] owners;
        FIRInfo firInfo;
    }

    struct FIRInfo {
        string firNo;
        string district;
        string year;
        string reason;
    }

    mapping(string => OwnerInfo) aadharToOwnerInfo;
    mapping(string => VehicleInfo) uniqueIDToVehicleInfo;

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
        OwnerInfo2 memory _ownerInfo2
    ) public {
        if (uniqueIDToVehicleInfo[_uniqueID].exists == true) {
            if (aadharToOwnerInfo[_aadhar].exists == true) {
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp;
                aadharToOwnerInfo[_aadhar] = OwnerInfo(
                    true,
                    _fName,
                    _lName,
                    _aadhar,
                    _dob,
                    _gender,
                    temp,
                    _ownerInfo2
                );
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
            }
        } else {
            if (aadharToOwnerInfo[_aadhar].exists == true) {
                string[] memory temp;
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(
                    true,
                    _uniqueID,
                    _vehicleNo,
                    _modelName,
                    _vehicleColor,
                    temp,
                    FIRInfo("", "", "", "")
                );
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
            } else {
                string[] memory temp1;
                string[] memory temp2;
                aadharToOwnerInfo[_aadhar] = OwnerInfo(
                    true,
                    _fName,
                    _lName,
                    _aadhar,
                    _dob,
                    _gender,
                    temp1,
                    _ownerInfo2
                );
                aadharToOwnerInfo[_aadhar].vehicles.push(_uniqueID);
                uniqueIDToVehicleInfo[_uniqueID] = VehicleInfo(
                    true,
                    _uniqueID,
                    _vehicleNo,
                    _modelName,
                    _vehicleColor,
                    temp2,
                    FIRInfo("", "", "", "")
                );
                uniqueIDToVehicleInfo[_uniqueID].owners.push(_aadhar);
            }
        }
    }

    function storeFirInfo(
        string memory _uniqueID,
        string memory _firNo,
        string memory _district,
        string memory _year,
        string memory _reason
    ) public {
        uniqueIDToVehicleInfo[_uniqueID].firInfo = FIRInfo(
            _firNo,
            _district,
            _year,
            _reason
        );
    }

    function getOwnerInfoFromAadhar(string memory _aadhar)
        public
        view
        returns (OwnerInfo memory ownerInfo)
    {
        return (aadharToOwnerInfo[_aadhar]);
    }

    function getVehicleInfoFromUniqueID(string memory _uniqueID)
        public
        view
        returns (VehicleInfo memory vehicleInfo)
    {
        return (uniqueIDToVehicleInfo[_uniqueID]);
    }

    function getVehiclesFromAadhar(string memory _aadhar)
        public
        view
        returns (string[] memory)
    {
        return aadharToOwnerInfo[_aadhar].vehicles;
    }

    function getOwnersFromUniqueID(string memory _uniqueID)
        public
        view
        returns (string[] memory)
    {
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
        aadharToOwnerInfo[_aadhar].ownerInfo2.email = _email;
        aadharToOwnerInfo[_aadhar].ownerInfo2.mobileNo = _mobileNo;
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
}
