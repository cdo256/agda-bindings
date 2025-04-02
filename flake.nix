{
  description = "Use agda bindings in Obsidian.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    just-agda.url = "github:cdo256/just-agda";
  };

  outputs =
    inputs:
    let
      inherit (inputs) nixpkgs;
      inherit (nixpkgs.lib.attrsets)
        mapAttrs
        mergeAttrsList
        ;
      inherit (nixpkgs.lib) genAttrs;
      systems = [ "x86_64-linux" ];
      forEachSystem =
        fn:
        mergeAttrsList (
          map (
            system:
            let
              res = fn nixpkgs.legacyPackages.${system};
            in
            mapAttrs (name: value: {
              ${system} = value;
            }) res
          ) systems
        );
    in
    forEachSystem (
      pkgs:
      let
        agda = pkgs.agda.withPackages (ps: [
          # TODO: Packages needed?
          #ps.standard-library
        ]);
        just-agda = inputs.just-agda.packages.${pkgs.system}.default;
      in
      {
        packages = {
          inherit agda just-agda;
          default = just-agda;
        };
        devShells.default = pkgs.mkShell {
          buildInputs = [
            agda
            just-agda
          ];
        };
      }
    );
}
