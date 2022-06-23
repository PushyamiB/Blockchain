pragma solidity ^0.4.22;

contract UserCrud {
  
  struct UserStruct {
    string organisation;
    uint RegNo;
    string name;
    string course;
    uint index;
    
  }
  uint certificate;
  mapping(uint => UserStruct) private userStructs;
  uint[] private userIndex;
  event LogNewUser   (uint  certificate, uint index, string organisation, uint RegNo);
  event LogUpdateUser(uint  certificate, uint index, string organisation, uint RegNo);
  function isUser(uint certificate)
    public
    constant
    returns(bool isIndeed)
  {
    if(userIndex.length == 0) return false;
    return (userIndex[userStructs[certificate].index] == certificate);
  }

  function insertUser(  
    uint certificate,
    uint RegNo,
    string organisation,
    string name,
    string course)
    public
    returns(uint index)
  {
    if(isUser(certificate)) throw;
    userStructs[certificate].organisation = organisation; 
    userStructs[certificate].RegNo=RegNo;
    userStructs[certificate].name   = name;
    userStructs[certificate].course = course;
    userStructs[certificate].index  = userIndex.push(certificate)-1;
    LogNewUser(
        certificate,
        userStructs[certificate].index,
        organisation,
        RegNo);
    return userIndex.length-1;
  }
  function getUser(uint certificate)
    public
    constant
    returns(string organisation, uint RegNo, uint index, string name, string course)
  {
    if(!isUser(certificate)) throw;
    return(
      userStructs[certificate].organisation,
      userStructs[certificate].RegNo,
      userStructs[certificate].index,
      userStructs[certificate].name,
      userStructs[certificate].course);
  }
    
  function getUserCount()
    public
    constant
    returns(uint count)
  {
    return userIndex.length;
  }
  
 function getUserAtIndex(uint index)
    public
    constant
    returns( uint,uint ,string , uint , string , string )
  {
    uint Certificate=userIndex[index];
    UserStruct storage u = userStructs[Certificate];
    return (u.index,Certificate,u.organisation,u.RegNo,u.name,u.course);
  }
}
/*function getUserAtIndex(uint index)
    public
    constant
    returns(uint certificate)
  {
    return userIndex[index];
  }
  
    
    
   function retrieveUsers() 
    public
    constant  
    returns (string organisation, uint RegNo, uint index, string name, string course)
    {
        for (uint i=0; i<=userIndex.length;i++){
               if (userStructs[certificate].index== i){
                    return (
                        userStructs[certificate].organisation,
                        userStructs[certificate].RegNo,
                        userStructs[certificate].index,
                        userStructs[certificate].name,
                        userStructs[certificate].course);
               }
        }
        

    }*/

 /* function updateUserName(uint certificate, string name)
    public
    returns(bool success)
  {
    if(!isUser(certificate)) throw;
    userStructs[certificate].name = name;
    LogUpdateUser(
      certificate,
      userStructs[certificate].index,
      userStructs[certificate].organisation,
      userStructs[certificate].RegNo);
    return true;
  }*/
  /*function updateUserAge(address userAddress, uint userAge)
    public
    returns(bool success)
  {
    if(!isUser(userAddress)) throw;
    userStructs[userAddress].userAge = userAge;
    LogUpdateUser(
      userAddress,
      userStructs[userAddress].index,
      userStructs[userAddress].userEmail,
      userAge);
    return true;
  }*/
  

