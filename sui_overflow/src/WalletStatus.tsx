import { useCurrentAccount } from "@mysten/dapp-kit";
import { Container, Flex, Heading, Text } from "@radix-ui/themes";
import { OwnedObjects } from "./OwnedObjects";
import api from "./backend/api";
import { useState, useEffect } from "react";

export function WalletStatus() {
  const account = useCurrentAccount();
  const [coinList, setCoinList] = useState<string[]>([]);
  useEffect(() => {
    api.getSuiCoinList().then((data) => setCoinList(data));
  }, []);


  return (
    <Container my="2">
      <Heading mb="2">Wallet Status</Heading>

      {account ? (
        <Flex direction="column">
          <Text>Wallet connected</Text>
          <Text>Address: {account.address}</Text>
          
        </Flex>
      ) : (
        <Text>Wallet not connected</Text>
      )}
      <Flex direction="column">
        <Text>CoinList: {coinList}</Text>
      </Flex>
      <OwnedObjects />
    </Container>
  );
}
