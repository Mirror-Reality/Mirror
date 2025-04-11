import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { MirrorReality } from "../target/types/mirror_reality";
import { expect } from "chai";

describe("mirror-reality", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.MirrorReality as Program<MirrorReality>;
  const mirrorAccount = anchor.web3.Keypair.generate();

  it("Creates a new mirror", async () => {
    const ipfsHash = "QmTestHash";
    await program.methods
      .createMirror(ipfsHash)
      .accounts({
        mirrorAccount: mirrorAccount.publicKey,
        owner: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([mirrorAccount])
      .rpc();

    const mirror = await program.account.digitalMirror.fetch(mirrorAccount.publicKey);
    expect(mirror.ipfsHash).to.equal(ipfsHash);
    expect(mirror.owner.toString()).to.equal(provider.wallet.publicKey.toString());
    expect(mirror.isActive).to.be.true;
  });

  it("Updates a mirror", async () => {
    const newIpfsHash = "QmNewHash";
    await program.methods
      .updateMirror(newIpfsHash)
      .accounts({
        mirrorAccount: mirrorAccount.publicKey,
        owner: provider.wallet.publicKey,
      })
      .rpc();

    const mirror = await program.account.digitalMirror.fetch(mirrorAccount.publicKey);
    expect(mirror.ipfsHash).to.equal(newIpfsHash);
  });

  it("Deactivates a mirror", async () => {
    await program.methods
      .deactivateMirror()
      .accounts({
        mirrorAccount: mirrorAccount.publicKey,
        owner: provider.wallet.publicKey,
      })
      .rpc();

    const mirror = await program.account.digitalMirror.fetch(mirrorAccount.publicKey);
    expect(mirror.isActive).to.be.false;
  });
}); 