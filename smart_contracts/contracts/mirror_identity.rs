use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    program_error::ProgramError,
    pubkey::Pubkey,
    program_pack::{IsInitialized, Pack, Sealed},
};
use borsh::{BorshDeserialize, BorshSerialize};

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct DigitalMirror {
    pub ipfs_hash: String,
    pub owner: Pubkey,
    pub created_at: i64,
    pub last_updated: i64,
    pub is_active: bool,
}

impl Sealed for DigitalMirror {}
impl IsInitialized for DigitalMirror {
    fn is_initialized(&self) -> bool {
        self.is_active
    }
}

impl Pack for DigitalMirror {
    const LEN: usize = 32 + 32 + 8 + 8 + 1;

    fn pack_into_slice(&self, dst: &mut [u8]) {
        let data = self.try_to_vec().unwrap();
        dst[..data.len()].copy_from_slice(&data);
    }

    fn unpack_from_slice(src: &[u8]) -> Result<Self, ProgramError> {
        let mut p = src;
        DigitalMirror::deserialize(&mut p).map_err(|_| ProgramError::InvalidAccountData)
    }
}

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("Processing instruction");

    let account_info_iter = &mut accounts.iter();
    let mirror_account = next_account_info(account_info_iter)?;
    let owner_account = next_account_info(account_info_iter)?;

    if !owner_account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let mut mirror = DigitalMirror::unpack_unchecked(&mirror_account.data.borrow())?;

    match instruction_data[0] {
        0 => {
            // Create mirror
            if mirror.is_active {
                return Err(ProgramError::AccountAlreadyInitialized);
            }

            let ipfs_hash = String::from_utf8(instruction_data[1..].to_vec())
                .map_err(|_| ProgramError::InvalidInstructionData)?;

            mirror = DigitalMirror {
                ipfs_hash,
                owner: *owner_account.key,
                created_at: Clock::get()?.unix_timestamp,
                last_updated: Clock::get()?.unix_timestamp,
                is_active: true,
            };
        }
        1 => {
            // Update mirror
            if !mirror.is_active {
                return Err(ProgramError::AccountNotInitialized);
            }

            if mirror.owner != *owner_account.key {
                return Err(ProgramError::IllegalOwner);
            }

            let ipfs_hash = String::from_utf8(instruction_data[1..].to_vec())
                .map_err(|_| ProgramError::InvalidInstructionData)?;

            mirror.ipfs_hash = ipfs_hash;
            mirror.last_updated = Clock::get()?.unix_timestamp;
        }
        2 => {
            // Deactivate mirror
            if !mirror.is_active {
                return Err(ProgramError::AccountNotInitialized);
            }

            if mirror.owner != *owner_account.key {
                return Err(ProgramError::IllegalOwner);
            }

            mirror.is_active = false;
            mirror.last_updated = Clock::get()?.unix_timestamp;
        }
        _ => return Err(ProgramError::InvalidInstructionData),
    }

    DigitalMirror::pack(mirror, &mut mirror_account.data.borrow_mut())?;
    Ok(())
} 