import {
  Flex,
  GridItem,
  Input,
  InputGroup,
  InputLeftElement,
  Link,
  Modal,
  ModalBody,
  ModalContent,
  ModalOverlay,
  useDisclosure,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { Station } from "../../types";
import { SearchIcon } from "@chakra-ui/icons";

export function SearchStationsModal({ stations }: { stations: Station[] }) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [filteredItems, setFilteredItems]: Station[] | any = useState(stations);
  return (
    <>
      <InputGroup onClick={onOpen} width={{ base: "full", sm: "fit-content" }}>
        <InputLeftElement
          pointerEvents="none"
          height={"full"}
          children={<SearchIcon color="black" />}
        />
        <Input
          placeholder="Tasteaza numele statiei"
          size="lg"
          width={{ base: "100%", sm: 280, lg: 350 }}
        />
      </InputGroup>

      <Modal isOpen={isOpen} onClose={onClose} size={"3xl"}
             preserveScrollBarGap={true}>
        <ModalOverlay />
        <ModalContent p={5}>
          <InputGroup mb={5}>
            <InputLeftElement
              pointerEvents="none"
              height={"full"}
              children={<SearchIcon color="black" />}
            />
            <Input
              placeholder="Tasteaza numele statiei"
              size="lg"
              width={{ base: "100%" }}
              onChange={e => {
                let filterText = e.target.value.toString().toLowerCase();
                let dataFiltered = stations.filter(
                  item =>
                    item.title.toLowerCase().toString().includes(filterText) &&
                    item,
                );
                setFilteredItems(dataFiltered);
              }}
            />
          </InputGroup>
          <ModalBody maxHeight={{ base: "calc(100vh - 230px)", sm: 600 }}
                     overflow="auto"
                     p={0} pr={3}>
            {filteredItems.length > 0 ? (
              <Flex flexDirection={"column"}>
                {filteredItems.map((station: Station) => (
                  <Link href={station.slug} px={2} py={3} m={1}
                        key={station.title}
                        _hover={{ background: "#00000013", borderRadius: 10 }}>
                    <a>{station.title}</a>
                  </Link>
                ))}
              </Flex>
            ) : (
              <GridItem as="div" colSpan={5} py={2}>
                Nu există nici o stație cu acest nume.
              </GridItem>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
}