pragma solidity ^0.4.22;

contract UserCrud {
  
  struct UserStruct {
    string organisation;
    uint RegNo;
    string name;
    string course;
    uint index;
    string datetime;
    string email;
  }
  uint certificate;
  mapping(uint => UserStruct) private userStructs;
  uint[] private userIndex;
  event LogNewUser   (uint  certificate, uint index, string organisation, uint RegNo, string email,string datetime);
  event LogUpdateUser(uint  certificate, uint index, string organisation, uint RegNo ,string email,string datetime);
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
    string course,
    string email,
    string datetime)
    public
    returns(uint index)
  {
    if(isUser(certificate)) throw;
    userStructs[certificate].organisation = organisation; 
    userStructs[certificate].RegNo=RegNo;
    userStructs[certificate].name   = name;
    userStructs[certificate].course = course;
    userStructs[certificate].index  = userIndex.push(certificate)-1;
    userStructs[certificate].email = email;
    userStructs[certificate].datetime = datetime;
    LogNewUser(
        certificate,
        userStructs[certificate].index,
        organisation,
        RegNo,email,datetime);
    return userIndex.length-1;
  }
  function getUser(uint certificate)
    public
    constant
    returns(string organisation, uint RegNo, uint index, string name, string course,string email,string datetime)
  {
    if(!isUser(certificate)) throw;
    return(
      userStructs[certificate].organisation,
      userStructs[certificate].RegNo,
      userStructs[certificate].index,
      userStructs[certificate].name,
      userStructs[certificate].course,
      userStructs[certificate].email,
      userStructs[certificate].datetime);
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
    returns( uint,uint ,string , uint , string , string ,string,string)
  {
    uint Certificate=userIndex[index];
    UserStruct storage u = userStructs[Certificate];
    return (u.index,Certificate,u.organisation,u.RegNo,u.name,u.course,u.email,u.datetime);
  }
}
